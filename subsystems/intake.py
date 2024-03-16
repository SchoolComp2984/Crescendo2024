#making a class for the robot's intake
#neo motors
from rev import CANSparkMax

class Intake:
    #initializing the intake
    def __init__(self, _intake_motor : CANSparkMax):
        #reference for the intake motor
        self.intake_motor = _intake_motor

    def intake_spin(self, speed):
        #spins the intake motor
        self.intake_motor.set(-speed)

    def stop(self):
        #stops the intake motors
        self.intake_motor.set(0)