# Linear Velocity: m/s
# Angular Velocity: rad/s
class Velocity:
  def __init__(self, velocity):
    self.linear = velocity[0:3]
    self.angular = velocity[3:6]

  def round(self, lPrec, aPrec):
    self.linear = [round(v, lPrec) for v in self.linear]
    self.angular = [round(v, aPrec) for v in self.angular]

  def __repr__(self):
    return repr(
        [
          self.linear[0], 
          self.linear[1], 
          self.linear[2], 
          self.angular[0], 
          self.angular[1], 
          self.angular[2], 
        ]
      )

# PWM: 8 byte
# Velocity: rad/s
class Motor:
  def __init__(self, pwmEast, pwmWest):
    self.setPwm(pwmEast, pwmWest)

  def setPwmEast(self, pwmEast):
    self.pwmEast = int(min(max(pwmEast, 0), 255))
    self.velEast = self.__toVelocity(self.pwmEast)

  def setPwmWest(self, pwmWest):
    self.pwmWest = int(min(max(pwmWest, 0), 255))
    self.velWest = self.__toVelocity(self.pwmWest)

  def setPwm(self, pwmEast, pwmWest):
    self.setPwmEast(pwmEast)
    self.setPwmWest(pwmWest)

  def getPwm(self):
    return self.pwmEast, self.pwmWest
  
  def getVelocity(self):
    return self.velEast, self.velWest
  
  # Audio estimated velocity of the motor.
  def __toVelocity(self, pwm):
    if pwm < 65:
      return 0
    pwm_2 = pwm * pwm
    pwm_3 = pwm_2 * pwm
    pwm_4 = pwm_3 * pwm
    pwm_5 = pwm_4 * pwm
    a = 2.158718e-08
    b = -2.016865e-05
    c = 7.315375e-03
    d = -1.294141e+00
    e = 1.142787e+02
    f = -2.961941e+03
    return a * pwm_5 + b * pwm_4 + c * pwm_3 + d * pwm_2 + e * pwm + f

  def __repr__(self):
    return repr([self.pwmEast, self.pwmWest])

# Meter
class Position:
  def __init__(self, position):
    self.position = position

  def round(self, lPrec):
    self.position = [round(v, lPrec) for v in self.position]

  def __repr__(self):
    return repr(self.position)

# NA
class Orientation:
  def __init__(self, orientation):
    self.orientation = orientation

  def __repr__(self):
    return repr(self.orientation)
