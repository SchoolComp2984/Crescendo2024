#Making a class for the shooter mechanism on the robot.
#the shooter motor is a neo.
class Shooter:
    #intiating the shooter
    def __init__(self, _shooter_motor):
        #creating a reference to our shooter motor
        self.shooter_motor = _shooter_motor

    #spins the shooting motor
    def shooter_spin(self, speed):
        self.shooter_motor.set(speed)