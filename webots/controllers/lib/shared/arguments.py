from enum import Enum, IntEnum
import enum
from os import times
import os
from typing import List, Tuple

IDENTIFIER = "-"

class ArgType(IntEnum):
  Float = 0
  Floats = 1
  Integer = 2
  Integers = 3
  String = 4
  Strings = 5

  def parseArgs(self, arguments):
    if self == ArgType.Float:
      return float(arguments[0])
    elif self == ArgType.Floats:
      return [float(arg) for arg in arguments]
    elif self == ArgType.Integer:
      return int(arguments[0])
    elif self == ArgType.Integers:
      return [int(arg) for arg in arguments]
    elif self == ArgType.String:
      return arguments[0]
    elif self == ArgType.Strings:
      return arguments

class ArgInfo:
  def __init__(self, field: str, type: ArgType):
    self.field = field
    self.type = type

class ArgParse:
  def parse(sysargs: List[str], *args: Tuple[ArgInfo]):
    arguments = dict()
    current = None
    for arg in sysargs:
      if arg.startswith(IDENTIFIER) and not arg[1:].isdigit():
        field = arg[1:]
        for argInfo in args:
          if field == argInfo.field:
            current = field
            arguments[current] = []
            break
      else:
        if current is not None:
          arguments[current].append(arg)
    vals = []
    for key in arguments.keys():
      for argInfo in args:
        if key == argInfo.field:
          vals.append(argInfo.type.parseArgs(arguments[key]))

    return vals
