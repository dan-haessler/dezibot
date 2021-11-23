import struct
import sys
import os
from controller import Robot

# Adding shared library.
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(os.path.join(os.path.dirname(ROOT_PATH), "lib")))

from shared.types import Motor

class Dezibot(Robot):
  def __init__(self):
    super().__init__()
    self.name = self.getName()
    self.motor = Motor(0, 0)
    self.hasMotor = False
    self.motorEast = self.getDevice("motorEast")
    self.motorWest = self.getDevice("motorWest")
    self.emitter = self.getDevice("emitter")
    self.__emitMotorPwm()
    if self.motorEast and self.motorWest:
      self.motorEast.setPosition(float('+inf'))
      self.motorWest.setPosition(float('+inf'))
      self.motorEast.setVelocity(0.0)
      self.motorWest.setVelocity(0.0)
      self.hasMotor = True

  def getRobotName(self) -> str:
    return self.name

  def getPwm(self) -> int:
    return self.motor.getPwm()

  def setPwm(self, pwmEast, pwmWest):
    self.motor.setPwm(pwmEast, pwmWest)
    self.__emitMotorPwm()

  def setPwmEast(self, pwmEast):
    self.motor.setPwmEast(pwmEast)
    self.__emitMotorPwm()

  def setPwmWest(self, pwmWest):
    self.motor.setPwmWest(pwmWest)
    self.__emitMotorPwm()
  
  # Emitting name up to 16 chars and pwm vals
  def __emitMotorPwm(self):
    nameLength = len(self.name)
    if nameLength > 0 and nameLength < 17:
      mEastPwm, mWestPwm = self.motor.getPwm()
      id = [bytes(char, 'utf-8') for char in self.name]
      for i in range(len(id), 16):
        id.append(bytes(' ', 'utf-8'))
      self.emitter.send(struct.pack("16cii", *id, mEastPwm, mWestPwm))

  def _setVelocity(self):
    # Send PWM signals to dezimaster
    if self.hasMotor:
      mEastVel, mWestVel = self.motor.getVelocity()
      self.motorEast.setVelocity(mEastVel)
      self.motorWest.setVelocity(mWestVel)

class DezibotController():
  def __init__(self):
    self.dezibot = Dezibot()
    self.timeStep = int(self.dezibot.getBasicTimeStep())

  # returns timestep in ms
  def getTimeStep(self) -> int:
    return self.timeStep

  # dezibot as extended webots robot
  def getDezibot(self) -> Dezibot:
    return self.dezibot

  def logError(self, text):
    sys.stdout.write(self.dezibot.name + "\033[31m" + " > " + "\033[0m" + text + "\n")

  def logSuccess(self, text):
    sys.stdout.write(self.dezibot.name + "\033[32m" + " > " + "\033[0m" + text + "\n")
  
  def logInfo(self, text):
    sys.stdout.write(self.dezibot.name + "\033[34m" + " > " + "\033[0m" + text + "\n")

  # Overwrite this
  def update(self):
    pass

  # Overwrite this
  def finish(self):
    pass
  
  def start(self):
    while self.dezibot.step(self.timeStep) != -1:
      self.update()
      self.getDezibot()._setVelocity()
    return self.finish()