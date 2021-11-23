import sys
import os

# Adding library.
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(os.path.join(os.path.dirname(ROOT_PATH), "lib")))

from shared.arguments import ArgParse, ArgType, ArgInfo
from shared.resource import Resources
from robot import DeziMaster

class Controller(DeziMaster):
  def __init__(self, ids, length, fields):
    super().__init__(ids, length, fields)
    self.resources = Resources()

  def update(self):
    # Tracking all robots.
    for id, dezibot in self.robots.items():
      entry = self.track(dezibot)
      self.resources.addEntry(id, entry)

  def finish(self):
    # Saving entries.
    saved = self.resources.save(ROOT_PATH)
    self.logSuccess("Saving: " + ", ".join(saved))

# Parsing webots configurable controller args.
(ids, fields, length) = ArgParse.parse(sys.argv,
  ArgInfo("id", ArgType.Strings),
  ArgInfo("track", ArgType.Strings),
  ArgInfo("length", ArgType.Integer)
)

# Starting and searching for arg given dezibots.
dezigod = Controller(ids, length, fields)
dezigod.logInfo("Searching: " + ", ".join(ids))
dezigod.logSuccess("Found: " + ", ".join(dezigod.robots.keys()))
dezigod.logInfo("Tracking: " + ", ".join(fields))
dezigod.logInfo("Length: " + str(length) + "ms")
dezigod.logInfo("Timestep: " + str(dezigod.timeStep) + "ms")
dezigod.start()
