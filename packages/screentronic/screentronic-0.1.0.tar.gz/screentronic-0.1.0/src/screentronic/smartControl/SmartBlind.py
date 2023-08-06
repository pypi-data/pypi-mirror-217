
import time
from .SmartControl import *

class SmartBlind():

  longHoldTime = 0.5

  def __init__(self, controlGroup: ControlGroup, controlType: ControlType, smartControl: SmartControl) -> None:
    self.controlGroup = controlGroup
    self.controlType = controlType
    self.smartControl = smartControl

  def __repr__(self) -> str:
    return f"SmartBlind({self.controlType.name} {self.controlGroup})"
  
  def up(self):
    if self.controlType == ControlType.SC:
      self.smartControl.sendRequest( SCPosition(self.controlGroup, 0, 255) )
    elif self.controlType == ControlType.DC:
      self.smartControl.sendRequest( ButtonPkt(self.controlGroup, ControlCmdDC.SwitchUpLong) )
      time.sleep( self.longHoldTime )
      self.smartControl.sendRequest( ButtonPkt(self.controlGroup, ControlCmdDC.SwitchUpRelease, longDownTime=self.longHoldTime, longDownTimeThreshold=self.longHoldTime) )
    else:
      raise NotImplementedError("This should be unreachable! You did not check all ControlType's!")

  def down(self):
    if self.controlType == ControlType.SC:
      self.smartControl.sendRequest( SCPosition(self.controlGroup, 255, 255) )
    elif self.controlType == ControlType.DC:
      self.smartControl.sendRequest( ButtonPkt(self.controlGroup, ControlCmdDC.SwitchDownLong) )
      time.sleep( self.longHoldTime )
      self.smartControl.sendRequest( ButtonPkt(self.controlGroup, ControlCmdDC.SwitchDownRelease, longDownTime=self.longHoldTime, longDownTimeThreshold=self.longHoldTime) )
    else:
      raise NotImplementedError("This should be unreachable! You did not check all ControlType's!")

  def set_position(self, height: int, angle: int):
    assert 0 <= height and height < 256
    assert 0 <= angle and angle < 256
    if self.controlType == ControlType.SC:
      self.smartControl.sendRequest( SCPosition(self.controlGroup, height, angle) )
    elif self.controlType == ControlType.DC:
      raise ValueError("The position functions are only supported on SC blinds!")
    else:
      raise NotImplementedError("This should be unreachable! You did not check all ControlType's!")

  def height(self, height: int):
    assert 0 <= height and height < 256
    current_height, current_angle = self.position()
    self.set_position( height, current_angle )

  def angle(self, angle: int):
    assert 0 <= angle and angle < 256
    current_height, current_angle = self.position()
    self.set_position( current_height, angle )

  def position(self) -> Tuple[int, int]:
    response = self.smartControl.sendRequest( SCStatusRequestPkt(self.controlGroup), timeout=1 )
    if isinstance(response, SCStatusResponsePkt):
      # response is a tuple of (height, angle)
      return (response.height, response.slats)
    else:
      raise ValueError(f"Failed to retrieve posistion! Expected a {SCStatusResponsePkt.__name__} but got: {response}")
