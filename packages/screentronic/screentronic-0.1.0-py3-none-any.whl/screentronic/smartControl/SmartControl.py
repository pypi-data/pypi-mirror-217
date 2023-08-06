from __future__ import annotations

import abc
import enum
import random
import logging
from typing import ByteString, Optional, Tuple

from ..UdpInterface import UdpInterface, split_data

## Byte 11
class CommandType(enum.Enum):
  AppControlCommand   = 16    # 0x10
  SwitchInputCommand  = 17    # 0x11
  StatusRequest       = 32    # 0x20
  StatusResponse      = 33    # 0x21
  def __repr__(self) -> str:
    return self.name

## Byte 12
class ControlType(enum.Enum):
  DC = 32  # 0x20
  SC = 37  # 0x25
  def __repr__(self) -> str:
    return self.name

## Byte 13
class ControlCmdSC(enum.Enum):
  ReadData              = 0  # 0x00
  Position              = 80 # 0x50
  Referencing           = 96 # 0x60
  def __repr__(self) -> str:
    return self.name

## Byte 13
class ControlCmdDC(enum.Enum):
  SwitchUpShort         = 1  # 0x01
  SwitchUpLong          = 2  # 0x02
  SwitchUpRelease       = 3  # 0x03
  SwitchDownShort       = 17 # 0x11
  SwitchDownLong        = 18 # 0x12
  SwitchDownRelease     = 19 # 0x13

ControlGroup = Tuple[int, int, int, int]

class SmartControlPacket():

  def __init__(self, controlGroup: ControlGroup, packetId: Optional[int] = None) -> None:
    self.packetId = packetId if packetId is not None else random.randint(0, 0xff)
    self.controlGroup = controlGroup

  def bytes(self, duplicate: int = 1) -> ByteString:
    # This is the header
    data = bytearray([
      ord('C'),             # Constant
      ord('T'),             # Constant
      17,                   # 17 = ControlGroup packet
      1,                    # ???
      self.controlGroup[0], # Control group ID Byte 1
      self.controlGroup[1], # Control group ID Byte 2
      self.packetId,        # Packet counter
      duplicate,            # Packet repeat counter, sometimes the same packet is sent multiple times (sine udp is unreliable). The only difference between duplicate packets is this counter that is incremented. New packets always start at 1
      0,                    # Frame length (auto calculated later on)
      self.controlGroup[2], # Control group ID Byte 3
      self.controlGroup[3], # Control group ID Byte 4
      # 0,                  # Command type
      # 0,                  # Control type
      # 0,                  # Control command
      # 0,                  # Data byte 1
      # 0,                  # Data byte 2
    ])
    
    data.extend( self.packetData() )

    # Calculate and add the checksum
    data[8] = len(data) + 2
    data.append( sum(iter(data)) & 0xff )
    data.append( 10 )

    return data

  @abc.abstractmethod
  def packetData(self) -> ByteString:
    pass

  @classmethod
  def parse( cls, data: ByteString ) -> Optional[SmartControlPacket]:
    if data[0] != 67 or data[1] != 84:
      raise ValueError("Expected 'CT' in the beginning of the packet!")
    pktLength = data[8]
    if len(data) != pktLength:
      raise ValueError(f"Expected a packet of {pktLength} bytes, but received {len(data)} bytes of data! {data=}")
    pid = data[6]
    controlGroup = (data[4],data[5],data[9],data[10])
    payload = data[11:(pktLength-2)]
    return cls._parse_payload( payload, pid, controlGroup )
    
  @abc.abstractclassmethod
  def _parse_payload( cls, payload: ByteString, packetId: int, controlGroup: ControlGroup ) -> Optional[SmartControlPacket]:
    pass

class SCPosition(SmartControlPacket):
  def __init__(self, controlGroup: ControlGroup, height: int, slats: int, direction: CommandType = CommandType.AppControlCommand, packetId: Optional[int] = None) -> None:
    super().__init__(controlGroup=controlGroup, packetId=packetId)
    self.height = height
    self.slats = slats
    self.direction = direction

  @classmethod
  def _parse_payload( cls, payload: ByteString, packetId: int, controlGroup: ControlGroup ) -> Optional[SmartControlPacket]:
    if payload[1] == ControlType.SC.value and payload[2] == ControlCmdSC.Position.value:
      return SCPosition(controlGroup, payload[3], payload[4], CommandType._value2member_map_.get(payload[0]), packetId=packetId)
    return None

  def packetData(self) -> ByteString:
    return bytes([
      self.direction.value,         # Command type
      ControlType.SC.value,         # Control type
      ControlCmdSC.Position.value,  # Control command
      self.height,                  # Data byte 1
      self.slats,                   # Data byte 2
    ])

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(controlGroup={self.controlGroup}, {self.height=}, {self.slats=}, {self.direction=})"

class SCReference(SmartControlPacket):
  def __init__(self, controlGroup: ControlGroup, height: int, slats: int, direction: CommandType = CommandType.AppControlCommand, packetId: Optional[int] = None) -> None:
    super().__init__(controlGroup=controlGroup, packetId=packetId)
    self.direction = direction
    self.height = height
    self.slats = slats

  @classmethod
  def _parse_payload( cls, payload: ByteString, packetId: int, controlGroup: ControlGroup ) -> Optional[SmartControlPacket]:
    if payload[1] == ControlType.SC.value and payload[2] == ControlCmdSC.Referencing.value:
      return SCReference(controlGroup, payload[3], payload[4], CommandType._value2member_map_.get(payload[0]), packetId=packetId)
    return None

  def packetData(self) -> ByteString:
    return bytes([
      self.direction.value,     # Command type
      ControlType.SC.value,     # Control type
      ControlCmdSC.Reference,   # Control command
      self.height,              # Data byte 1
      self.slats,               # Data byte 2
    ])
  
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(controlGroup={self.controlGroup}, {self.height=}, {self.slats=}, {self.direction=})"

class SCStatusRequestPkt(SmartControlPacket):
  @classmethod
  def _parse_payload( cls, payload: ByteString, packetId: int, controlGroup: ControlGroup ) -> Optional[SmartControlPacket]:
    if payload[0] == CommandType.StatusRequest.value and payload[1] == ControlType.SC.value and payload[2] == ControlCmdSC.ReadData.value:
      return SCStatusRequestPkt(controlGroup, packetId=packetId)
    return None

  def packetData(self) -> ByteString:
    return bytes([
      CommandType.StatusRequest.value, # Command type
      ControlType.SC.value,         # Control type
      ControlCmdSC.ReadData.value, # Control command
      0x00,                         # Data byte 1
      0x00,                         # Data byte 2
    ])
  
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(controlGroup={self.controlGroup})"

class SCStatusResponsePkt(SmartControlPacket):
  def __init__(self, controlGroup: ControlGroup, control: int = 0x21, height: int = 0x00, slats: int = 0x00, packetId: Optional[int] = None) -> None:
    super().__init__(controlGroup=controlGroup, packetId=packetId)
    self.control = control
    self.height = height
    self.slats = slats

  @classmethod
  def _parse_payload( cls, payload: ByteString, packetId: int, controlGroup: ControlGroup ) -> Optional[SmartControlPacket]:
    if payload[0] == CommandType.StatusResponse.value and (payload[1] == 0x21 or payload[1] == 0x22):
      return SCStatusResponsePkt(controlGroup, payload[1], payload[3], payload[4], packetId=packetId )
    return None

  def packetData(self) -> ByteString:
    return bytes([
      CommandType.StatusResponse.value, # Command type
      self.control,                     # ???
      0x00,                             # ???
      self.height,                      # Data byte 1
      self.slats,                       # Data byte 2
    ])
  
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(controlGroup={self.controlGroup}, control={self.control}, height={self.height}, slats={self.slats})"

class ButtonPkt(SmartControlPacket):
  def __init__(self, 
               controlGroup: ControlGroup, 
               buttonCmd: ControlCmdDC, 
               fromApp: bool = True, 
               control: ControlType = ControlType.DC, 
               longDownTime: float = None,                    # Time in [s], Required for SwitchUpRelease / SwitchDownRelease
               longDownTimeThreshold: float = 0.5,            # Time in [s], Used in SwitchUpRelease / SwitchDownRelease
               packetId: Optional[int] = None) -> None:
    super().__init__(controlGroup=controlGroup, packetId=packetId)
    if buttonCmd in [ ControlCmdDC.SwitchUpRelease, ControlCmdDC.SwitchDownRelease ]:
      assert longDownTime is not None
    self.buttonCmd = buttonCmd
    self.fromApp = fromApp
    self.control = control
    self.longDownTime = longDownTime
    self.longDownTimeThreshold = longDownTimeThreshold

  @classmethod
  def _parse_payload( cls, payload: ByteString, packetId: int, controlGroup: ControlGroup ) -> Optional[SmartControlPacket]:
    commandType = CommandType._value2member_map_.get(payload[0])
    control = ControlType._value2member_map_.get(payload[1])

    if not (commandType == CommandType.SwitchInputCommand or (commandType == CommandType.AppControlCommand and control == ControlType.DC)):
      return None

    press = ControlCmdDC._value2member_map_.get(payload[2])

    if commandType == CommandType.AppControlCommand:
      fromApp = True
    elif commandType == CommandType.SwitchInputCommand:
      fromApp = False
    else:
      raise ValueError(f"Expected button command to have either commandType == ({CommandType.AppControlCommand.name} or {CommandType.SwitchInputCommand.name}) but got {commandType.name}!")

    longDownTime = None
    longDownTimeThreshold = None
    if press in [ControlCmdDC.SwitchUpShort, ControlCmdDC.SwitchUpLong]:
      assert payload[3] == 0 or payload[3] == 6 # These are the only values I've seen
      assert payload[4] == 0
    elif press in [ControlCmdDC.SwitchDownShort, ControlCmdDC.SwitchDownLong]:
      assert payload[3] == 1 or payload[3] == 6 # These are the only values I've seen
      assert payload[4] == 0
    elif press in [ControlCmdDC.SwitchUpRelease, ControlCmdDC.SwitchDownRelease]:
      longDownTime = payload[3] / 10.0
      longDownTimeThreshold = payload[4] / 10.0
    else:
      raise ValueError("This should not be possible! Did we check all possible ControlCmdDC command types???")

    return ButtonPkt(controlGroup, press, fromApp, control, longDownTime, longDownTimeThreshold, packetId)

  def packetData(self) -> ByteString:
    if self.buttonCmd in [ControlCmdDC.SwitchUpShort, ControlCmdDC.SwitchUpLong]:
      data0 = 0
      data1 = 0
    elif self.buttonCmd in [ControlCmdDC.SwitchDownShort, ControlCmdDC.SwitchDownLong]:
      data0 = 1
      data1 = 0
    elif self.buttonCmd in [ControlCmdDC.SwitchUpRelease, ControlCmdDC.SwitchDownRelease]:
      data0 = min(int(self.longDownTime * 10), 255) & 0xff
      data1 = min(int(self.longDownTimeThreshold * 10), 255) & 0xff

    return bytes([
      (CommandType.AppControlCommand if self.fromApp else CommandType.SwitchInputCommand).value,
      self.control.value,
      self.buttonCmd.value,
      data0,
      data1
    ])
  
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(controlGroup={self.controlGroup}, buttonCmd={self.buttonCmd}, fromApp={self.fromApp}, control={self.control}, longDownTime={self.longDownTime}, longDownTimeThreshold={self.longDownTimeThreshold})"


class SmartControl():

  default_timeout = 0.25

  def __init__(self, udpInterface: UdpInterface = UdpInterface()) -> None:
    self.udpInterface = udpInterface

  def __repr__(self) -> str:
    return f"SmartControl()"

  def blind( self, controlGroup: ControlGroup, controlType: ControlType = ControlType.SC ) -> 'SmartBlind':
    from .SmartBlind import SmartBlind
    return SmartBlind(controlGroup, controlType, self)

  def sendRequest( self, packet: SmartControlPacket, timeout: Optional[int] = None, duplicates: int=1 ) -> Optional[SmartControlPacket]:
    """ Sends a packet out to this ST2134 module reads the response back """
    response = self._sendRequest(packet, self.udpInterface, timeout=timeout, duplicates=duplicates, counterOffset=None)
    return response

  @classmethod
  def _sendRequest( cls, packet: SmartControlPacket, udpInterface: UdpInterface, timeout: Optional[int] = None, duplicates: int=1, counterOffset: Optional[int] = 0 ) -> Optional[SmartControlPacket]:
    """ Sends a packet out over the given udp interface and reads the response back """
    logging.debug(f"Sending: {packet}")
    for i in range(duplicates):
      if counterOffset is not None:
        packet.packetId = counterOffset + i
      udpInterface.write( packet.bytes(duplicate=i+1) )
    response = cls._readPacket( udpInterface, timeout )
    if response:
      # Flush any duplicates we might get
      while dup := cls._readPacket( udpInterface, timeout ):
        pass
    return response

  @classmethod
  def _readPacket( cls, udpInterface: UdpInterface, timeout: Optional[int] = None ):
    """Tries to read a single UDP packet from the given udp interface"""
    try:
      data = udpInterface.read(timeout=timeout or cls.default_timeout)
      for subdata in split_data( data ):
        return parse_control_group_packet(subdata)
    except TimeoutError:
      return None

def parse_control_group_packet(data: ByteString) -> SmartControlPacket|None:
  types = [SCPosition, SCReference, SCStatusRequestPkt, SCStatusResponsePkt, ButtonPkt]
  for type in types:
    pkt = type.parse(data)
    if pkt is not None:
      return pkt
  return None
