from subsystems.arm import Arm

from wpilib import Timer

class Climb:
    def __init__(self, _arm : Arm):
        self.arm = _arm

        self.IDLE = 0
        self.MOVING = 1
        self.FINISHED = 2
        self.stage = self.IDLE

        self.timer = Timer()
        self.climbing_start_time = 0.0

        self.running = False

    def climb(self):
        if not self.running:
            return
        
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.MOVING
            self.climbing_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.MOVING:
            self.arm.set_speed(-1)

            if self.climbing_start_time + 7 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.running = False

    