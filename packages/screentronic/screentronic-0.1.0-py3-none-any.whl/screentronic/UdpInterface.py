
import re
import sys
import struct
import socket
from typing import ByteString

controltronic_address = "224.0.43.54"
controltronic_port = 43541

def controltronicSocket(address: str, port: int) -> socket.socket:
  # Open the udp multicast socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.settimeout(0.025)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  if sys.platform == 'win32':
    s.bind(('', port))
  else:
    s.bind((address, port))
  mreq = struct.pack("4sl", socket.inet_aton(address), socket.INADDR_ANY)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)
  return s

# Splits a UDP payload data into a stream of controltronic packets
#  Each packet starts with b'CT' and ends with b'\n'
def split_data(data: bytes):
  for match in re.finditer(br"CT.+?\n(?=(C|\Z))", data, re.DOTALL):
    yield match.group(0)

class UdpInterface:

  def __init__(self, address: str = controltronic_address, port: int = controltronic_port) -> None:
    self.address = address
    self.port = port
    self.socket = controltronicSocket( address, port )

  def peek(self, len: int = 10240, timeout: int = 0.025) -> ByteString:
    self.socket.settimeout(timeout)
    return self.socket.recv(len, socket.MSG_PEEK)

  def read(self, len: int = 10240, timeout: int = 0.025) -> ByteString:
    try:
      self.socket.settimeout(timeout)
      #print(f"Buffer now has: " + str(self.peek()))
      return self.socket.recv(len)
    except socket.timeout as e:
      raise TimeoutError() from e

  def write(self, data: ByteString) -> None:
    if isinstance(data, bytes) or isinstance(data, ByteString):
      bytes_data = data
    elif isinstance(data, list):
      bytes_data = bytes(data)
    else:
      raise NotImplementedError()
    
    self.socket.sendto(bytes_data, (self.address, self.port))
    # Drain the socket of what we just sent
    rxData = self.peek(len(bytes_data))
    if rxData == bytes_data:
      self.read(len(bytes_data))
