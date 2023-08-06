from __future__ import annotations

import abc
import enum
import logging
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
  from Blind import Blind

class BmcType(enum.Enum):
  UNKNOWN  = 0
  MB       = 1631      # = 57345 is in the response string # ScreenLine MB blind
  ST2161   = 2511      # = 57346 is in the response string # ScreenTronic ST2161

class Parameter():
  def __init__(self, register: int, register_index: int) -> None:
    self.register = register
    self.register_index = register_index
  def get( self, ct: ControlTronic, nodeId: int ):
    return ct._parameterGet( 0, nodeId, self.register, self.register_index )

class StringParameter(Parameter):
  pass

class IntParameter(Parameter):
  def get( self, ct: ControlTronic, nodeId: int ):
    result = super().get(ct, nodeId)
    if result is not None:
      return int(result)
    else:
      return result

class FloatParameter(Parameter):
  def __init__(self, register: int, register_index: int, scale: float = 1.0) -> None:
    super().__init__(register, register_index)
    self.scale = scale
  def get( self, ct: ControlTronic, nodeId: int ):
    result = super().get(ct, nodeId)
    if result is not None:
      return float(result) * self.scale
    else:
      return result

class HeightAngleParameter(IntParameter):
  def get( self, ct: ControlTronic, nodeId: int ):
    result = super().get(ct, nodeId)
    if result is not None:
      result = int(result)
      return (
        result & 0xff,           # Height
        ((result & 0xff00) >> 8) # Angle
      )
    else:
      return result

class StatusParameter(IntParameter):
  def get( self, ct: ControlTronic, nodeId: int ):
    result = super().get(ct, nodeId)
    if result is None:
      return None
    self.status = int(result) & 0xFFFFFF
    return {
      "target_reached"             : (self.status >>  0) & 1,
      "moving_up"                  : (self.status >>  3) & 1,
      "moving_down"                : (self.status >>  4) & 1,
      "referencing"                : (self.status >>  5) & 1,
      "following_err"              : (self.status >>  8) & 1,
      "following_err_ref"          : (self.status >>  9) & 1,
      "blocked_window_contact"     : (self.status >> 16) & 1,
      "blocked_new_config"         : (self.status >> 17) & 1,
      "blocked_following_err"      : (self.status >> 18) & 1,
      "blocked_following_err_ref"  : (self.status >> 19) & 1
    }

class AddressParameter(Parameter):
  def get( self, ct: ControlTronic, blindId: int ):
    result = super().get(ct, blindId)
    if result is None:
      return None
    try:
      return int(result)
    except:
      if result == "Error: -542":
        return 57345
      elif result == "Error: -583":
        return -1
    raise ValueError("Unexpected address response: " + result)

class HallSensorParameter(IntParameter):
  def get( self, ct: ControlTronic, nodeId: int ):
    result = super().get(ct, nodeId)
    if result is None:
      return None
    info = {
      0: "0 0 0 (invalid state?)",
      1: "1 0 0",
      2: "0 1 0",
      3: "1 1 0",
      4: "0 0 1",
      5: "1 0 1",
      6: "0 1 1",
      7: "1 1 1 (invalid state?)"
    }
    return result, info.get(result, "-")

class Parameters(enum.Enum):
  Voltage                     = StringParameter(12560, 0)
  #P2                          = StringParameter(12561, 0)
  #P3                          = StringParameter(12562, 0)
  #Current                     = StringParameter(12563, 0)
  Current                     = StringParameter(12563, 0)
  TemperatureOutputStage      = FloatParameter(12564, 0, 1.0/10.0)
  Speed                       = StringParameter(14852, 0)
  #P8                          = StringParameter(20746, 1)
  #P9                          = StringParameter(20748, 2)
  Pos                         = StringParameter(14178, 0)
  #P11                         = StringParameter(20576, 0)
  RefLimit                    = IntParameter(20576, 7)
  # ConfigWrite                 = lambda value: value # Generic
  InfoID                      = IntParameter(20737, 1)
  InfoVersion                 = IntParameter(20737, 2)
  InfoFirmwareMSB             = IntParameter(12323, 0)
  InfoFirmwareLSB             = IntParameter(12323, 1)
  InfoConfig                  = IntParameter(20576, 10)
  #InfoTerminal                = lambda value: int(value) # <= This is a generic request
  HeightAngle                 = HeightAngleParameter(20739, 2) # 0x5103 # (height, angle)
  Status                      = StatusParameter(20738, 2)
  ParameterSetResponse        = IntParameter(12335, 1)
  ProductionInfoD0            = IntParameter(12335, 1)
  ProductionInfoD1            = IntParameter(12335, 2)
  ProductionInfoD2            = IntParameter(12335, 3)
  ProductionInfoD3            = IntParameter(12335, 4)
  # ParameterError1             = lambda value: value.lower() != "ok" # Generic
  # ParameterError2             = lambda value: value.lower() != "ok" # Generic
  # Feedback                    = lambda value: value.lower() == "ok" # Generic
  InfoTemperatureOutputStage  = IntParameter(12564, 0)
  InfoCurrentFiltered         = IntParameter(12898, 1)
  InfoVoltageControl          = FloatParameter(12560, 0, 1.0 / 1000.0)
  InfoCounterMoveCommands     = IntParameter(14754, 71)
  InfoCounterTiltCommands     = IntParameter(14754, 70)
  InfoPowerDownVoltage        = IntParameter(14754, 33)
  InfoHallSensor              = HallSensorParameter(12584, 0)
  StateProg                   = IntParameter(20742, 1) # Referencing done if value != 80 && value != 81
  InfoLength                  = IntParameter(20752, 1)
  InfoPosition                = IntParameter(14178, 0)
  InfoEeLength                = IntParameter(20576, 0)
  InfoEePosition              = IntParameter(20576, 1)
  InfoRef                     = IntParameter(14754, 68)
  #InfoRef                     = IntParameter(20576, 5)
  InfoRefCounter              = IntParameter(14754, 69)
  #InfoRefCounter              = IntParameter(20576, 6)
  InfoStatus                  = IntParameter(12290, 0)
  InfoError                   = IntParameter(12289, 0)
  InfoFollowing               = IntParameter(14179, 0)
  MotorParameterResult        = IntParameter(12332, 0) # 1129590833 == ok
  #ResultString                = StringParameter(xxxxxxx, xxxxxxx) ### [195] mc store ALL ### [195] mc set rs232_baudrate 57600
  AddressExists               = AddressParameter(12320, 0)
  ValueQAE0                   = IntParameter(14754, 64+ 0)
  ValueQAE1                   = IntParameter(14754, 64+ 1)
  ValueQAE2                   = IntParameter(14754, 64+ 2)
  ValueQAE3                   = IntParameter(14754, 64+ 3)
  ValueQAE4                   = IntParameter(14754, 64+ 4)
  ValueQAE5                   = IntParameter(14754, 64+ 5)
  ValueQAE6                   = IntParameter(14754, 64+ 6)
  ValueQAE7                   = IntParameter(14754, 64+ 7)
  ValueQAE8                   = IntParameter(14754, 64+ 8)
  ValueQAE9                   = IntParameter(14754, 64+ 9)
  ValueQAE10                  = IntParameter(14754, 64+10)
  ValueQAE11                  = IntParameter(14754, 64+11)
  ValueQAE12                  = IntParameter(14754, 64+12)
  ValueQAE13                  = IntParameter(14754, 64+13)
  ValueQAE14                  = IntParameter(14754, 64+14)
  ValueQAE15                  = IntParameter(14754, 64+15)
  ValueCurrent0               = IntParameter(12836, 0)
  ValueCurrent1               = IntParameter(12836, 1)
  ValueCurrent2               = IntParameter(12836, 2)
  ValueCurrent3               = IntParameter(12836, 3)
  ConfigEEPROM0               = IntParameter(20576,  0)
  ConfigEEPROM1               = IntParameter(20576,  1)
  ConfigEEPROM2               = IntParameter(20576,  2)
  ConfigEEPROM3               = IntParameter(20576,  3)
  ConfigEEPROM4               = IntParameter(20576,  4)
  ConfigEEPROM5               = IntParameter(20576,  5)
  ConfigEEPROM6               = IntParameter(20576,  6)
  ConfigEEPROM7               = IntParameter(20576,  7)
  ConfigEEPROM8               = IntParameter(20576,  8)
  ConfigEEPROM9               = IntParameter(20576,  9)
  ConfigEEPROM10              = IntParameter(20576, 10)
  ConfigEEPROM11              = IntParameter(20576, 11)
  ConfigEEPROM12              = IntParameter(20576, 12)
  ConfigEEPROM13              = IntParameter(20576, 13)
  ConfigEEPROM14              = IntParameter(20576, 14)
  ConfigEEPROM15              = IntParameter(20576, 15)
  Temperature                 = StringParameter(20759, 1)


class ControlTronic(abc.ABC):
  """ This should be the same for the IP/KNX/Serial interface ? """

  def __init__(self) -> None:
      self._send_command("[88]  set sdo_timeout 200")

  @abc.abstractmethod
  def _send_command(self, command: str, timeout=1.0) -> Optional[str]:
    pass

  @abc.abstractmethod
  def blinds(self) -> List[Blind]:
    """Get a list of all connected blinds"""
    pass

  def info(self, blindId: int):
    logging.info(" Information request .... ")
    bmcType = self.addressExists(blindId)
    if bmcType is not None and bmcType != BmcType.UNKNOWN:
      logging.info(f"Blind connected to {blindId} is of type {bmcType.name}")
      infoFirmwareMSB = self.parameterGet(Parameters.InfoFirmwareMSB, blindId)
      infoFirmwareLSB = self.parameterGet(Parameters.InfoFirmwareLSB, blindId)
      if bmcType == BmcType.ST2161:
        logging.info("ScreenTronic ST2161")
        logging.info(f"Length: {self.parameterGet(Parameters.InfoLength, blindId)}")
        logging.info(f"Position: {self.parameterGet(Parameters.InfoPosition, blindId)}")
        logging.info(f"Reference: {self.parameterGet(Parameters.InfoRef, blindId)}")
        logging.info(f"Reference counter: {self.parameterGet(Parameters.InfoRefCounter, blindId)}")
        logging.info(f"Status: {self.parameterGet(Parameters.InfoStatus, blindId)}")
        logging.info(f"Error: {self.parameterGet(Parameters.InfoError, blindId)}")
        logging.info(f"Following state: {self.parameterGet(Parameters.InfoFollowing, blindId)}")
        logging.info(f"Move commands counter:{self.parameterGet(Parameters.InfoCounterMoveCommands, blindId)} / T:{self.parameterGet(Parameters.InfoCounterTiltCommands, blindId)}")
      else:
        logging.info("ScreenLine MB blind ")
        if (infoFirmwareMSB << 16 | infoFirmwareLSB) >= 26411174:
          logging.info(f"Voltage control: {self.parameterGet(Parameters.InfoVoltageControl, blindId):.1f}")
          logging.info(f"Length: {self.parameterGet(Parameters.InfoLength, blindId)}")
          logging.info(f"Position: {self.parameterGet(Parameters.InfoPosition, blindId)}")
          logging.info(f"Reference: {self.parameterGet(Parameters.InfoRef, blindId)}")
          logging.info(f"Reference counter: {self.parameterGet(Parameters.InfoRefCounter, blindId)}")
          logging.info(f"Status: {self.parameterGet(Parameters.InfoStatus, blindId)}")
          logging.info(f"Error: {self.parameterGet(Parameters.InfoError, blindId)}")
          logging.info(f"Following state: {self.parameterGet(Parameters.InfoFollowing, blindId)}")
          logging.info(f"Hall sensor: {self.parameterGet(Parameters.InfoHallSensor, blindId)[1]}")
          logging.info(f"Move commands counter: {self.parameterGet(Parameters.InfoCounterMoveCommands, blindId)} / T:{self.parameterGet(Parameters.InfoCounterTiltCommands, blindId)}")
        else:
          logging.info(f"Length: {self.parameterGet(Parameters.InfoLength, blindId)}")
          logging.info(f"Position: {self.parameterGet(Parameters.InfoPosition, blindId)}")
          logging.info(f"ELength: {self.parameterGet(Parameters.InfoEeLength, blindId)}")
          logging.info(f"EPosition: {self.parameterGet(Parameters.InfoEePosition, blindId)}")
          logging.info(f"Reference: {self.parameterGet(Parameters.InfoRef, blindId)}")
          logging.info(f"Reference counter: {self.parameterGet(Parameters.InfoRefCounter, blindId)}")
          logging.info(f"Reference limit: {self.parameterGet(Parameters.InfoRefLIMIT, blindId)}")
          logging.info(f"Status: {self.parameterGet(Parameters.InfoStatus, blindId)}")
          logging.info(f"Error: {self.parameterGet(Parameters.InfoError, blindId)}")
          logging.info(f"Following state: {self.parameterGet(Parameters.InfoFollowing, blindId)}")
          logging.info(f"Hall sensor: {self.parameterGet(Parameters.InfoHallSensor, blindId)[1]}")
    elif bmcType is not None:
      logging.info("Device does not have anything connected there, or its device model is unknown!")
    else:
      logging.info("Device is NOT responding!")

  def parameterGet(self, parameter: Parameters, blindId: int) -> Optional[Any]:
    for i in range(0, 3):
      resp = parameter.value.get( self, blindId )
      if resp:
        return resp
    return resp

  def _parameterGet(self, parameter: int, blindId: int, register: int, register_index: int) -> Optional[str]:
    command = f"[{parameter:02d}] {blindId} r 0x{register:04x} {register_index} i32"
    #command = f"[{parameter:02d}] {blindId} r 0x{register:04x} 0x{register_index:x} i32"
    response = self._send_command( command )
    if response is not None:
      if response.startswith(f"[{parameter:05d}]") or response.startswith(f"[{parameter:02d}]"):
        out = response[response.index(']')+2:]
        return out
      else:
        logging.warning(f"Expected response to command '{command}' to start with the same sequence nr, but got: {response}")
    return None

  def addressExists(self, address: int) -> Optional[BmcType]:
    info = self.addressDetect(address)
    return info is not None and info != BmcType.UNKNOWN

  def addressDetect(self, address: int) -> Optional[BmcType]:
    result = self.parameterGet(Parameters.AddressExists, address)
    if result is None:
      return None
    elif result == 57346:
      return BmcType.ST2161
    elif result == 57345:
      return BmcType.MB
    else:
      return BmcType.UNKNOWN
