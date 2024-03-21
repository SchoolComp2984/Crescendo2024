from phoenix5._ctre import WPI_TalonSRX

from wpilib import Timer

class Climb:
    def __init__(self, _climb_motor_left_front : WPI_TalonSRX, _climb_motor_right_front : WPI_TalonSRX, _climb_motor_left_back : WPI_TalonSRX, _climb_motor_right_back : WPI_TalonSRX):
        self.climb_motor_left_front = _climb_motor_left_front
        self.climb_motor_right_front = _climb_motor_right_front
        self.climb_motor_left_back = _climb_motor_left_back
        self.climb_motor_right_back = _climb_motor_right_back

        self.timer = Timer()

        self.IDLE = 0
        self.RETRACTING = 1
        self.FINISHED = 2
        self.stage = self.IDLE

        self.retracting_start_time = 0.0

        self.retracting = False

    def climb_spin(self, speed):
        self.climb_motor_left_front.set(speed)
        self.climb_motor_right_front.set(-speed)
        self.climb_motor_left_back.set(speed)
        self.climb_motor_right_back.set(-speed)


    def stop(self):
        self.climb_spin(0)
    