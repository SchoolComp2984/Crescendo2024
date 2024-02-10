#making a class for the robot's intake
#neo motors
class Intake:
    #initializing the intake
    def __init__(self, _intake_motor):
        #reference for the intake motor
        self.intake_motor = _intake_motor

    def intake_spin(self, speed):
        #spins the intake motor
        self.intake_motor.set(-speed)

    def stop(self):
        self.intake_motor.set(0)