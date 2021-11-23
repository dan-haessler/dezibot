import sys
import os
import struct
from typing import List

# Adding library.
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(os.path.join(os.path.dirname(ROOT_PATH), "lib")))

from controller import Supervisor
from shared.types import Position, Velocity, Motor, Orientation
from shared.resource import Entry, Field

class DeziSlave():
  def __init__(self, robot):
    self.robot = robot
    self.motor = Motor(0, 0)

  def setMotor(self, motor):
    self.motor = motor

  def getPosition(self):
    return Position(self.robot.getPosition())

  def getOrientation(self):
    return Orientation(self.robot.getOrientation())

  def getVelocity(self):
    return Velocity(self.robot.getVelocity())

  def getMotor(self):
    return self.motor

class DeziMaster(Supervisor):
  def __init__(self, ids, length, fields):
    super().__init__()
    self.length = length
    self.fields = fields
    self.robots = dict()
    self.receiver = self.getDevice("receiver")
    self.receiver.enable(int(self.getBasicTimeStep()))
    self.timeStep = int(self.getBasicTimeStep())
    self.currentTime = 0
    self.lastHeartbeat = 0
    self.heartbeatTime = length / 10
    self.register(ids)

  def register(self, ids: List[str]):
    for id in ids:
      robot = self.getFromDef(id)
      if robot:
        self.robots[id] = DeziSlave(robot)
    return self.robots

  def track(self, robot):
    entry = Entry()
    if Field.Time.value in self.fields:
      entry.time = self.currentTime
    if Field.Position.value in self.fields:
      entry.position = robot.getPosition()
    if Field.Orientation.value in self.fields:
      entry.orientation = robot.getOrientation()
    if Field.Velocity.value in self.fields:
      entry.velocity = robot.getVelocity()
    if Field.Motor.value in self.fields:
      entry.motor = robot.getMotor()
    return entry

  def receiveMessages(self):
    while (self.receiver.getQueueLength() > 0):
      message = self.receiver.getData()
      dataList = struct.unpack("16cii", message)
      id = ''.join([char.decode('utf-8') for char in dataList[0:16]]).strip()
      pwmEast = dataList[16]
      pwmWest = dataList[17]
      self.robots[id].setMotor(Motor(pwmEast, pwmWest))
      self.receiver.nextPacket()

  def heartbeat(self):
    if self.lastHeartbeat + self.heartbeatTime <= self.currentTime:
      self.lastHeartbeat = self.currentTime
      message = "{:1.1f}%".format(self.currentTime / self.length * 100) + " - " + str(self.currentTime) + " ms / " + str(self.length) + " ms."
      self.logSuccess(message)

  def logError(self, text):
    sys.stdout.write("\033[34m" + "DEZIMASTER" + "\033[31m" + " > " + "\033[0m" + text + "\n")

  def logSuccess(self, text):
    sys.stdout.write("\033[34m" + "DEZIMASTER" + "\033[32m" + " > " + "\033[0m" + text + "\n")
  
  def logInfo(self, text):
    sys.stdout.write("\033[34m" + "DEZIMASTER" + "\033[34m" + " > " + "\033[0m" + text + "\n")

  def update(self):
    pass

  def finish(self):
    pass

  def start(self):
    self.receiveMessages()
    self.update()
    while self.step(self.timeStep) != -1:
      self.currentTime = int(round(self.getTime() * 1000, 0))
      if self.length <= self.currentTime:
        break
      self.receiveMessages()
      self.update()
      self.heartbeat()
      
    return self.finish()
