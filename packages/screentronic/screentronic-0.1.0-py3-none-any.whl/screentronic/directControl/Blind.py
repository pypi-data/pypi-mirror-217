
import enum
import time
from typing import TYPE_CHECKING, Tuple
from .ControlTronic import ControlTronic, Parameters

class Blind:

  class BlindCommand(enum.Enum):
    NOOP                  = (0x5102, 1, 0)
    NEW                   = (0x5102, 1, 5)
    NEW_SPECIAL           = (0x5102, 1, 6)
    UP                    = (0x5102, 1, 10)
    UP_FAST               = (0x5102, 1, 11)
    UP_FREE               = (0x5102, 1, 12)
    UP_STEP               = (0x5102, 1, 15)
    DOWN                  = (0x5102, 1, 20)
    DOWN_FAST             = (0x5102, 1, 21)
    DOWN_FREE             = (0x5102, 1, 22)
    DOWN_STEP             = (0x5102, 1, 25)
    STOP                  = (0x5102, 1, 30)
    POS_TRANSPORT_BLIND   = (0x5102, 1, 40)
    POS_TRANSPORT_GLASS   = (0x5102, 1, 41)
    POS_TRANSPORT_DRYING  = (0x5102, 1, 45)
    HOMING_UP             = (0x5102, 1, 50)
    HOMING_DOWN           = (0x5102, 1, 51)
    GOTO_HEIGHT_ANGLE     = (0x5102, 1, 100) # This seems buggy ?
    GOTO_HEIGHT           = (0x5102, 1, 101)
    GOTO_ANGLE            = (0x5102, 1, 102)

  def __init__(self, ct: ControlTronic, blindId: int) -> None:
    self.ct = ct
    self.blindId = blindId
    self.blindType = ct.addressDetect(self.blindId)

  def __repr__(self) -> str:
    return f"Blind({self.blindType.name} {self.blindId})"
  
  def _sendBlindCommand( self, cmd: BlindCommand ):
    (register, registerSubindex, value) = cmd.value
    self.ct._send_command(f"{self.blindId} w 0x{register:04x} {registerSubindex} i32 {value}")
    time.sleep(0.2)

  def _goto(self):
    self._sendBlindCommand( self.BlindCommand.GOTO_HEIGHT )
    time.sleep(0.2)
    self._sendBlindCommand( self.BlindCommand.GOTO_ANGLE )
    time.sleep(0.2)

  def up(self):
    self._sendBlindCommand( self.BlindCommand.UP )

  def up_fast(self):
    self._sendBlindCommand( self.BlindCommand.UP_FAST )

  def up_free(self):
    self._sendBlindCommand( self.BlindCommand.UP_FREE )

  def up_step(self):
    self._sendBlindCommand( self.BlindCommand.UP_STEP )

  def down(self):
    self._sendBlindCommand( self.BlindCommand.DOWN )

  def down_fast(self):
    self._sendBlindCommand( self.BlindCommand.DOWN_FAST )

  def down_free(self):
    self._sendBlindCommand( self.BlindCommand.DOWN_FREE )

  def down_step(self):
    self._sendBlindCommand( self.BlindCommand.DOWN_STEP )

  def stop(self):
    self._sendBlindCommand( self.BlindCommand.STOP )

  def set_position(self, height: int, angle: int):
    assert 0 <= height and height < 256
    assert 0 <= angle and angle < 256
    self.ct._send_command(f"{self.blindId} w 0x5103 1 u32 0x0000{angle:02X}{height:02X}")
    self._goto()

  def height(self, height: int):
    assert 0 <= height and height < 256
    current_height, current_angle = self.position()
    self.ct._send_command(f"{self.blindId} w 0x5103 1 u32 0x0000{current_angle:02X}{height:02X}")
    self._goto()

  def angle(self, angle: int):
    assert 0 <= angle and angle < 256
    current_height, current_angle = self.position()
    self.ct._send_command(f"{self.blindId} w 0x5103 1 u32 0x0000{angle:02X}{current_height:02X}")
    self._goto()

  def position(self) -> Tuple[int, int]:
    response = self.ct.parameterGet(Parameters.HeightAngle, self.blindId)
    if response:
      # response is a tuple of (height, angle)
      return response
    else:
      raise ValueError("Failed to retrieve posistion!")

  def commandStatusRequest(self):
    return self.parameterGet(106, self.blindId, 0x5102, 2)

  def commandRefUp(self):
    self._sendBlindCommand( self.BlindCommand.HOMING_UP )

  def commandRefDown(self):
    self._sendBlindCommand( self.BlindCommand.HOMING_DOWN )
