from wpilib import Timer

class Shooter:
    def __init__(self, _shooter_lower_motor, _shooter_upper_motor):
        self.shooter_lower_motor = _shooter_lower_motor
        self.shooter_upper_motor = _shooter_upper_motor

    def shooter_spin(self, speed):
        self.shooter_lower_motor.set(speed)
        self.shooter_upper_motor.set(speed)

    def stop(self):
        self.shooter_spin(0)
