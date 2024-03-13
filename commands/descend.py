from wpilib import Timer

class Descend:
    def __init__(self, _arm):
        self.arm = _arm

        self.IDLE = 0
        self.MIDDLE = 1
        self.DELAY = 2
        self.DOWN = 3
        self.FINISHED = 4
        self.stage = self.IDLE

        self.timer = Timer()
        self.transition_delay_start_time = 0.0
        self.end_delay_start_time = 0.0

    def auto_descend(self):
        if self.stage == self.IDLE:
            self.stage = self.MIDDLE

        elif self.stage == self.MIDDLE:
            self.arm.desired_position = 15

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 8:
                self.stage = self.DELAY
                self.transition_delay_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.DELAY:
            if self.transition_delay_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.DOWN

        elif self.stage == self.DOWN:
            self.arm.desired_position = -10

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 5:
                self.stage = self.FINISHED
                self.end_delay_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.FINISHED:
            if self.end_delay_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.IDLE

