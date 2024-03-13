from wpilib import Timer

class Descend:
    def __init__(self, _arm):
        self.arm = _arm

        self.IDLE = 0
        self.MIDDLE = 1
        self.DOWN = 2
        self.FINISHED = 3
        self.stage = self.IDLE

        self.timer = Timer()
        self.end_delay = 0.0

    def auto_descend(self):
        if self.stage == self.IDLE:
            self.stage = self.MIDDLE

        elif self.stage == self.MIDDLE:
            self.arm.desired_position = 15

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 8:
                self.stage = self.DOWN

        elif self.stage == self.DOWN:
            self.arm.desired_position = -10

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 5:
                self.stage = self.FINISHED
                self.end_delay = self.timer.getFPGATimestamp()

        elif self.stage == self.FINISHED:
            if self.end_delay + 1 < self.timer.getFPGATimestamp():
                self.stage = self.IDLE

