# Webots

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

## Controllers
---
### Dezibot

The file [./controllers/dezibot/dezibot.py](./controllers/dezibot/dezibot.py) has an example of the usage. This is what you want! It is the program that gets executed for every dezibot in your world.

You can use this however you want but the intended usage is this one:
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
* Only necessary for technical reasons to track (also later to set the velocity), no need to look at this one [./controllers/dezibot/dezimaster.py](./controllers/dezibot/dezibot.py)
* Supervisor to track and set the velocity of the dezibots from a given model.
* Available tracking:
  * time
  * motor pwm
  * position
  * orientation
  * velocity
