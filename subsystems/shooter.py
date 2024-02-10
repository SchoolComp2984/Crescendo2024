#Making a class for the shooter mechanism on the robot.
#the shooter motor is a neo.

class Shooter:
    #intiating the shooter
    def __init__(self, _shooter_lower_motor, _shooter_upper_motor):
        #creating a reference to our shooter motor
        self.shooter_lower_motor = _shooter_lower_motor
        self.shooter_upper_motor = _shooter_upper_motor

   
    #spins the shooting motors
    def shooter_spin(self, speed):
        self.shooter_lower_motor.set(speed)
        self.shooter_upper_motor.set(-speed)

    def stop(self):
        self.shooter_lower_motor.set(0)
        self.shooter_upper_motor.set(0)

