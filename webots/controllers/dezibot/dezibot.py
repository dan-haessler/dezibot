import random
from robot import DezibotController

class Controller(DezibotController):
  def __init__(self):
    super().__init__()
    self.logSuccess("dezibot controller started.")
    self.logInfo("hello world!")

  # Every tick current pwm +- 50
  def update(self):
    dezibot = self.getDezibot()

    # Get current pwm
    mEastPwm, mWestPwm = dezibot.getPwm()

    # Get timestep
    # timeStep = self.getTimeStep()

    # Set pwm, everything outside of 0-255 gets rounded to nearest.
    newEastPwm = random.randrange(mEastPwm - 50, mEastPwm + 50)
    newWestPwm = random.randrange(mWestPwm - 50, mWestPwm + 50)

    # Use the setPwm function
    self.getDezibot().setPwm(newEastPwm, newWestPwm)
  
  def finish(self):
    self.logSuccess("Controller has finished.")

controller = Controller()
controller.start()
