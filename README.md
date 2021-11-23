# A 3D locomotion model.
This is a locomotion model for the dezibot v3.

# Basics

## Units/Coordinate System
coordinate system with EUN orientation so a position, velocity, acceleration consists of 6 DOF with following units:

|               | Linear   | Rotational |
|---------------|----------|------------|
| Position      | m        | rad        |
| Velocity      | m/s      | rad/s      |
| Accelaration  | m/s²     | rad/s²     |

So velocity could be described as followed:
```
V = [[1.0, 0.0, 1.0], [0.0, 0.0, 0.0]]
```
which means a velocity of 1m/s in x and z direction.

## Motor
The locomotion is based on two vibration motors which can be powered by a 8 byte PWM signal.

The voltage can be approximated by
```
U = PWM / 255 * 3,3
```

The angular velocity of the flywheel can be approximated by the following function:

![motor](./motor_rad.png)
