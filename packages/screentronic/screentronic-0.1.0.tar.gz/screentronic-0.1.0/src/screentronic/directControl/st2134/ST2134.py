from __future__ import annotations
import abc
import enum
import itertools
import logging
import time
import random
from typing import List, ByteString, Optional, Generator

from screentronic.UdpInterface import UdpInterface, controltronic_address, controltronic_port
from screentronic.directControl.ControlTronic import ControlTronic
from screentronic.directControl.Blind import Blind

class PowerChannel(enum.Enum):
  # What outputs to power on on the device
  All_On  = 1
  All_Off = 2
  CH_1    = 17
  CH_2    = 18
  CH_3    = 19
  CH_4    = 20
  def __repr__(self) -> str:
    return self.name

class ST2134Packet():
  def __init__(self, packetId: Optional[int] = None) -> None:
    super().__init__()
    # We use a random packet id instead of sequential counter
    # That way we can cut the link between the interface that needs to do the counting and the packet
    self.packetId = packetId if packetId is not None else random.randint(0, 0xff)

  def bytes(self, duplicate: int = 1) -> ByteString: 
    pass

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}"
  
# ----------------------------------
# ST2134DevicePacket
# ----------------------------------

class ST2134DevicePacket(ST2134Packet):

  def __init__(self, mac, packetType: int, packetId: Optional[int] = None) -> None:
    super().__init__(packetId=packetId)
    self.mac = mac
    self.packetType = packetType

  def bytes(self, duplicate: int = 1) -> ByteString: 
    # This is the header
    data = bytearray([
      ord('C'),         # Constant
      ord('T'),         # Constant
      0xff,             # Packet type
      1,                # ???
      1,                # ???
      1,                # ???
      self.packetId,    # Packet counter, to keep track of request and reponses that belong together
      1,                # Packet repeat counter, sometimes the same packet is sent multiple times (sine udp is unreliable). The only difference between duplicate packets is this counter that is incremented. New packets always start at 1
      17,               # Payload length (currently only header+crc, you still need to add the payload length)
      self.mac[0],      # Destination device mac address
      self.mac[1],      # Destination device mac address
      self.mac[2],      # Destination device mac address
      self.mac[3],      # Destination device mac address
      self.mac[4],      # Destination device mac address
      self.mac[5],      # Destination device mac address
    ])
    
    # Add the payload
    payload = bytearray( [self.packetType] ) + self.packetData()
    encrypted_payload = self.encrypt( payload )
    data.extend( encrypted_payload )
    data[8] += len(encrypted_payload)

    # Calculate and add the checksum
    data.append( sum(iter(data)) & 0xff )
    data.append( 10 )

    return data

  @abc.abstractmethod
  def packetData(self) -> ByteString:
    pass

  @classmethod
  def encrypt(cls, input: ByteString) -> ByteString:
    output = []
    password_b5  = input[3] if len(input) > 3 else 0 # The 5th byte is encoded using the 4th byte plain text
    password_b11 = input[6] if len(input) > 6 else 0 # The 11th byte is encoded using the 7th byte plain text
    password = itertools.chain(
      iter([86, 112, 13, 187, password_b5, 16, 242, 138, 209, 69, password_b11, 246, 117, 137, 45, 77, 127, 103, 205, 209, 112]),
      itertools.count(39)
    )
    for plain_text, secret in zip(input, password):
      output.append( cls.encrypt_byte(plain_text, secret) )
    return bytes(output)
  
  @classmethod
  def encrypt_byte( cls, input: int, secret: int ) -> int:
    return (input + secret) & 0xff

  @classmethod
  def decrypt(cls, input: ByteString) -> ByteString:
    password = itertools.chain(
      iter([86, 112, 13, 187, 0, 16, 242, 138, 209, 69, 0, 246, 117, 137, 45, 77, 127, 103, 205, 209, 112]),
      itertools.count(39)
    )
    output = []
    for cypher_text, secret in zip(input, password):
      output.append( cls.decrypt_byte(cypher_text, secret) )
    # Fix the 5th and 11th byte as these use the previous byte plain text as secret
    if len(output) > 4:
      output[4] = cls.decrypt_byte(input[4], output[3])
    if len(output) > 10:
      output[10] = cls.decrypt_byte(input[10], output[6])
    return bytes(output)

  @classmethod
  def decrypt_byte( cls, input: int, secret: int ) -> int:
    return (256 + input - secret) & 0xff

  def __eq__(self, other):
    return isinstance(other, ST2134DevicePacket) and self.mac == other.mac and self.packetType == other.packetType  and self.packetId == other.packetId
  def __hash__(self):
    return hash((self.mac, self.packetType, self.packetId))

class DiscoveryPacket(ST2134DevicePacket):
  def __init__(self, mac, packetId: Optional[int] = None) -> None:
    super().__init__(mac, 0, packetId=packetId)
  def packetData(self) -> ByteString:
    return bytes([0])

class PowerChannelPacket(ST2134DevicePacket):
  def __init__(self, mac, channel: PowerChannel, packetId: Optional[int] = None) -> None:
    super().__init__(mac, channel.value, packetId=packetId)
    self.channel = channel
  def packetData(self) -> ByteString:
    return bytes([self.channel.value])
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(channel={self.channel.name})"
  def __eq__(self, other):
    return isinstance(other, PowerChannelPacket) and super().__eq__(other) and self.channel == other.channel
  def __hash__(self):
    return hash((super().__hash__(), self.channel))

class IdentifyPacket(ST2134DevicePacket):
  def __init__(self, mac, packetId: Optional[int] = None) -> None:
    super().__init__(mac, 49, packetId=packetId)
  def packetData(self) -> ByteString:
    return bytes([49])

class CommandPacket(ST2134DevicePacket):
  def __init__(self, mac, command, packetId: Optional[int] = None) -> None:
    super().__init__(mac, 80, packetId=packetId)
    self.command = command
  
  def packetData(self) -> ByteString:
    return bytes(self.command, 'utf-8')

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.command=})"

  def __eq__(self, other):
    return isinstance(other, CommandPacket) and super().__eq__(other) and self.command == other.command

  def __hash__(self):
    return hash((super().__hash__(), self.command))

class StringResponsePacket(ST2134DevicePacket):
  def __init__(self, mac, string, packetId: Optional[int] = None) -> None:
    super().__init__(mac, 96, packetId=packetId)
    self.string = string
  
  def packetData(self) -> ByteString:
    return bytes(self.string, 'utf-8')

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.string=})"

  def __eq__(self, other):
    return isinstance(other, StringResponsePacket) and super().__eq__(other) and self.string == other.string

  def __hash__(self):
    return hash((super().__hash__(), self.string))




class ST2134(ControlTronic):

  default_timeout = 0.03
  min_inter_packet_time = 0.1

  def __init__(self, mac: List[int], udpInterface: UdpInterface = UdpInterface(controltronic_address, controltronic_port)) -> None:
    self.mac = mac
    self.mac_str = ':'.join(map(lambda m: f'{m:02x}',self.mac))
    self.udpInterface = udpInterface
    self.tlast = 0
    assert self.sendRequest(DiscoveryPacket(mac))
    assert self.sendRequest(PowerChannelPacket(mac, PowerChannel.All_On))
    super().__init__()

  def __repr__(self) -> str:
    return f"ST2134({self.mac_str})"

  def identify(self) -> Optional[str]:
    """Activate light and beep on this ST2134 module.
        Returns the version string of the module if found
    """
    logging.debug(f"Sending identify to {self}")
    response = self.sendRequest(IdentifyPacket(self.mac))
    if isinstance(response, StringResponsePacket):
      if 'ok' in response.string:
        version = response.string[2:]
        logging.info(f"Version of {self} is: {version}")
        return version
    logging.warning(f"Expected string response with 'ok' and the version, but got response: {response}")
    return None

  def blind( self, blindId: int ) -> Blind:
    return Blind(self, blindId)

  def blinds(self) -> List[Blind]:
    blinds = []
    for blindId in [ 127, 1, 2, 3, 4 ]:
      if self.addressExists( blindId ):
        blinds.append( Blind(self, blindId) )
    return blinds

  def blinds_all(self) -> Blind:
    return Blind(self, PowerChannel.All_On.value)

  def blinds_none(self) -> Blind:
    return Blind(self, PowerChannel.All_Off.value)

  def enableCommunicationToBlinds(self, channels: PowerChannel):
    resp = self.sendRequest( PowerChannelPacket( self.mac, channels ) )
    if resp is None:
      raise ValueError("Failed to select channel! No response received!")
    if isinstance(resp, StringResponsePacket):
      if resp.string.lower() == 'ok':
        return
    raise ValueError(f"Got an error response while switching address/channel: {resp=}")

  @classmethod
  def discover(cls, address: str = controltronic_address, port: int = controltronic_port) -> List[ST2134]:
    interface = UdpInterface(address, port)
    return cls.discover_on( interface )
  
  @classmethod
  def discover_on(cls, interface: UdpInterface) -> Generator[ST2134, None, None]:
    pktCounter = 0 # We do this as it makes it easier to lineup captures from python & cts
    # These are the first 4 bytes of all controltronic ethernet devices
    mac_base = [0x50, 0x4B, 0x5B, 0x81]
    # Here we iterate over all the possible macs that out device can have
    for mac5 in range(0, 12):
      for mac6 in range(0, 256):
        mac = mac_base + [mac5, mac6]
        mac_str = ':'.join(map(lambda m: f'{m:02x}',mac))
        logging.debug(f"Probing mac address {mac_str}")
        pkt = DiscoveryPacket(mac)
        response = cls._sendRequest(pkt, interface, counterOffset=pktCounter % 256)
        pktCounter += 1
        if isinstance(response, StringResponsePacket) and response.string == 'ok':
          logging.info(f"Found a device on mac address: {mac_str}")
          yield ST2134(mac, interface)
        elif response:
          logging.info(f"Received unexpected packet mac address {mac_str}: {response}")
  
  def sendRequest( self, packet: ST2134Packet, timeout: Optional[int] = None, duplicates: int=1 ) -> Optional[ST2134Packet]:
    """ Sends a packet out to this ST2134 module reads the response back """
    response = self._sendRequest(packet, self.udpInterface, timeout=timeout, duplicates=duplicates, counterOffset=None)
    return response

  @classmethod
  def _sendRequest( cls, packet: ST2134Packet, udpInterface: UdpInterface, timeout: Optional[int] = None, duplicates: int=1, counterOffset: Optional[int] = 0 ) -> Optional[ST2134Packet]:
    """ Sends a packet out over the given udp interface and reads the response back """
    logging.debug(f"Sending: {packet}")
    for i in range(duplicates):
      if counterOffset is not None:
        packet.packetId = counterOffset + i
      udpInterface.write( packet.bytes(duplicate=i) )
    response = cls._readPacket( udpInterface, timeout )
    if response:
      # Flush any duplicates we might get
      while dup := cls._readPacket( udpInterface ):
        pass
    return response

  @classmethod
  def _readPacket( cls, udpInterface: UdpInterface, timeout: Optional[int] = None ):
    """Tries to read a single UDP packet from the given udp interface"""
    try:
      data = udpInterface.read(timeout=timeout or cls.default_timeout)
      pktLength = data[8]
      if not len(data) == pktLength:
        logging.warning(f"Packet length encoded in the packet ({pktLength}) does not match the udp data length received ({len(data)})!")
      # Verify the crc
      crc_calc = sum(iter(data[:-2])) & 0xff
      if not data[-2] == crc_calc:
        raise EOFError(f"CRC mismatch on udp data! Calculated CRC={crc_calc} does not match the packet CRC of {data[-2]}! {data=}")
      if not data[-1] == 10:
        raise EOFError(f"EOF byte mismatch on udp data! Expected the last byte in the packet to be {10}, but that does not match the packet byte of {data[-1]}! {data=}")
      # Valid udp packet, 
      return cls._parseST2134Packet(data)
    except EOFError as e:
      logging.warning("We got garbled data!", exc_info=True)
      return None
    except TimeoutError:
      return None

  @classmethod
  def _parseST2134Packet( cls, data: ByteString ):
    if data[0] != 67 or data[1] != 84:
      raise ValueError("Expected 'CT' in the beginning of the packet!")
    pid = data[6]
    mac = data[9:14]

    pktLength = data[8]
    if len(data) != pktLength:
      raise ValueError(f"Expected a packet of {pktLength} bytes, but received {len(data)} bytes of data! {data=}")

    if data[2] == 0xff and data[3] == 1:
      encrypted_payload = data[15:(pktLength-2)]
      payload = ST2134DevicePacket.decrypt( encrypted_payload )

      if payload[0] == 0:
        return DiscoveryPacket(mac, packetId=pid)
      elif payload[0] in PowerChannel._value2member_map_.keys():
        channel = PowerChannel._value2member_map_.get(payload[0])
        return PowerChannelPacket( mac, channel=channel, packetId=pid )
      elif payload[0] == 49:
        return IdentifyPacket( mac, packetId=pid )
      elif payload[0] == 80:
        return StringResponsePacket( mac, payload[1:].decode(), packetId=pid )
      elif payload[0] == 96:
        return StringResponsePacket( mac, payload[1:].decode(), packetId=pid )
      else:
        raise ValueError(f"Unsupported payload type: {payload[0]}.\nNetwork bytes: {data.hex()}\nPayload: {payload}")

  def _send_command(self, command: str) -> Optional[str]:
    logging.debug(f"Sending command '{command}' to {self}")
    delay = (self.tlast + self.min_inter_packet_time) - time.time()
    if delay > 0:
      time.sleep(delay)
    response = self.sendRequest(CommandPacket(self.mac, command), timeout=1.0)
    self.tlast = time.time()
    if isinstance(response, StringResponsePacket):
      logging.debug(f"Command response is: {response.string}")
      return response.string
    logging.warning(f"Expected string response, but got response: {response}")
    return None

def parse_st2134_packet(data: ByteString) -> ST2134DevicePacket|None:
  try:
    return ST2134._parseST2134Packet(data)
  except ValueError:
    return None
