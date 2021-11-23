# Webots
Three protos/controller are relevant for this project.

## Dezibot
  * Three rigid legs
    * 2,5mm circle with 6 polygons (+- 0.05mm)
    * 20mm height (+- 0.10mm)
  * Circuit board
    * 25mm radius "perfect" circle (+- 0.15mm)
    * 1mm height (+- 0.05mm)
  * coordinate origin is the bottom center
  * Mass
    * 0.0275233g
    * Center of Mass? 
      * "guessed"
      * currently (20mm - 25mm, 20mm + 1mm, 0mm)
      * top side of circuit board with z near the uv led

## Motor control.
The [python controller for the dezibot](./controllers/dezibot/dezibot.py) is an example of the usage. It has a very simple structure. Have fun.
```
# Import 
from robot import DezibotController

class Controller(DezibotController):
  def __init__(self):
    super().__init__()
    # Load here

  def update(self):
    # Define the action within one timestep.
  
  def finish(self):
    # Do stuff when controller finished

# Execute
controller = Controller()
controller.start()

```
## Dezimaster
* Supervisor to track and set the velocity of the dezibots from a given model.
* Available tracking:
  * time
  * motor pwm
  * position
  * orientation
  * velocity
