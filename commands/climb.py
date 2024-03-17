from rev import CANSparkMax

class Climb:
    def __init__(self, _climb_motor : CANSparkMax):
        self.climb_motor = _climb_motor

    def climb_spin(self, speed):
        self.climb_motor.set(speed)
    