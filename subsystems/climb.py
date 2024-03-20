from phoenix5._ctre import WPI_TalonSRX

from wpilib import Timer

class Climb:
    def __init__(self, _climb_motor_left : WPI_TalonSRX, _climb_motor_right : WPI_TalonSRX):
        self.climb_motor_left = _climb_motor_left
        self.climb_motor_right = _climb_motor_right

        self.timer = Timer()

        self.IDLE = 0
        self.RETRACTING = 1
        self.FINISHED = 2
        self.stage = self.IDLE

        self.retracting_start_time = 0.0

        self.retracting = False

    def climb_spin(self, speed):
        self.climb_motor_left.set(speed)
        self.climb_motor_right.set(-speed)
    """
    def retract_climb(self):
        if self.stage == self.IDLE:
            self.stage = self.RETRACTING
            self.retracting_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.RETRACTING:
            self.climb_spin(-0.4)

            if self.retracting_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.RETRACTING

        elif self.stage == self.FINISHED:
            self.retracting = False
    """

    def stop(self):
        self.climb_spin(0)
    