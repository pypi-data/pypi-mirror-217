

#!/usr/bin/env python3

import logging
import asyncio_dgram
from cachetools import TTLCache 
from typing import Set, Generator, Union

from screentronic.UdpInterface import UdpInterface, split_data
from screentronic.directControl.st2134.ST2134 import parse_st2134_packet, ST2134Packet
from screentronic.smartControl.SmartControl import parse_control_group_packet, SmartControlPacket, ControlGroup


class Client():

  def __init__(self) -> None:
    self.interface = UdpInterface()
    self.duplicate_filter_history = TTLCache(maxsize=10, ttl=0.5)

  # Decodes UDP payload data into a stream of controltronic packets
  def _read_packets(self, data: bytes) -> Generator[Union[SmartControlPacket,ST2134Packet], None, None]:
    logging.debug( f"Received data on the UDP socket: {data.hex()}" )
    for subdata in split_data(data):
      try:
        pkt = parse_st2134_packet(subdata) or parse_control_group_packet( subdata )
        if pkt is not None:
          yield pkt
        else:
          logging.warning(f"Failed to decode packet!\n{data=}\n{subdata=}\n{subdata.hex()=}\n{list(subdata)=}", exc_info=True)
      except Exception as e:
        logging.warning(f"Failed to decode packet!\n{data=}\n{subdata=}\n{subdata.hex()=}\n{list(subdata)=}", exc_info=True)

  # This filters a packet stream removing duplicate received packets
  #  Basically discards duplicate packets that arive within 0.5s of the first packet
  def _duplicate_filter( self, pkt ):
    if self.duplicate_filter_history.__contains__(pkt):
      return False
    else:
      self.duplicate_filter_history[pkt] = True
      return True

  async def handle( self, pkt: Union[SmartControlPacket,ST2134Packet] ):
    logging.info(f"Packet: {pkt}")

  async def loop(self):
    # Connect to the multicast socket, the same one we use to send out stuff
    stream = await asyncio_dgram.from_socket( self.interface.socket )
    
    while True:
      data, _ = await stream.recv()
      for pkt in self._read_packets(data):
        if self._duplicate_filter( pkt ):
          await self.handle( pkt )

    stream.close()
