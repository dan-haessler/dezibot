from enum import Enum
import os
import numpy as np
from typing import List
from enum import Enum

class Field(Enum):
  Time = "time"
  Motor = "motor"
  Position = "position"
  Orientation = "orientation"
  Velocity = "velocity"

  def toHeader(fields, limiter=', '):
    return limiter.join([field.value for field in fields])

  def fromHeader(header: str, limiter=","):
    fields = []
    strFields = header.split(limiter)
    if Field.Time.value in strFields:
      fields.append(Field.Time)
    if Field.Motor.value in strFields:
      fields.append(Field.Motor)
    if Field.Position.value in strFields:
      fields.append(Field.Position)
    if Field.Orientation.value in strFields:
      fields.append(Field.Orientation)
    if Field.Velocity.value in strFields:
      fields.append(Field.Velocity)
    return fields

class Entry():
  def __init__(self, time=None, motor=None, position=None, orientation=None, velocity=None):
    self.time = time
    self.motor = motor
    self.position = position
    self.orientation = orientation
    self.velocity = velocity

  def getFromCsv(row, fields):
    rVal = row.split(',')
    entry = Entry()
    count = 0
    if Field.Time.value in fields:
      entry.time = float(rVal[count])
      count = count + 1
    if Field.Motor.value in fields:
      entry.motor = [int(rVal[count]), int(rVal[count+1])]
      count = count + 2
    if Field.Position.value in fields:
      entry.position = [float(rVal[count]), float(rVal[count+1]), float(rVal[count+2])]
      count = count + 3
    if Field.Orientation.value in fields:
      entry.orientation = [float(rVal[count]), float(rVal[count+1]), float(rVal[count+2])]
      count = count + 4
    if Field.Velocity.value in fields:
      entry.velocity = [
        [float(rVal[count]), float(rVal[count+1]), float(rVal[count+2])],
        [float(rVal[count+3]), float(rVal[count+4]), float(rVal[count+5])],
      ]
      count = count + 6
    return entry

  def getFields(self):
    fields = []
    if self.time is not None:
      fields.append(Field.Time)
    if self.motor is not None:
      fields.append(Field.Motor)
    if self.position is not None:
      fields.append(Field.Position)
    if self.orientation is not None:
      fields.append(Field.Orientation)
    if self.velocity is not None:
      fields.append(Field.Velocity)
    return fields
  
  def __repr__(self):
    output = []
    if self.time is not None:
      output.append(repr(self.time))
    if self.motor is not None:
      output.append(repr(self.motor))
    if self.position is not None:
      output.append(repr(self.position))
    if self.orientation is not None:
      output.append(repr(self.orientation))
    if self.velocity is not None:
      output.append(repr(self.velocity))
    return ", ".join(output)


class Resources():
  def __init__(self):
    self.runs = dict()

  def set(self, id: str, entries: List[Entry]):
    self.runs[id] = entries

  def addEntry(self, id: str, entry: Entry):
    if id in self.runs.keys():
      self.runs[id].append(entry)
    else:
      self.runs[id] = [entry]
  
  def get(self, id: str):
    if id in self.runs.keys():
      return self.runs[id] 

  def getEntryCount(self):
    return np.sum([len(run) for run in self.getRuns()])

  def getRuns(self):
    return self.runs.values()

  def save(self, path, outDir="output"):
    saved = []
    for id in self.runs.keys():
      run = self.runs[id]
      if len(run) == 0:
        continue
      outputDir = os.path.join(path, outDir)
      if not os.path.exists(outputDir):
        os.mkdir(outputDir)
        
      filePath = os.path.join(outputDir, str(id) + ".run")
      fields = run[0].getFields()
      with open(filePath, 'w+') as file:
        file.write(Field.toHeader(fields) + "\n")
        for entry in run:
          file.write(repr(entry) + "\n")
        saved.append(id)
    return saved

  def load(self, path):
    for fileName in os.listdir(path):
      name = fileName.split(".")[0]
      filePath = os.path.join(path, fileName)
      with open(filePath, 'r') as file:
        fields = Field.fromHeader(file.readline())
        entries = [Entry.getFromCsv(row, fields) for row in file.readlines()]
        self.set(name, entries)
