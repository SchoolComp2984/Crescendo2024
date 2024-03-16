from wpilib import Timer

class Descend:
    def __init__(self, _arm):
        self.arm = _arm

        self.IDLE = 0
        self.DOWN_1 = 1
        self.DELAY_1 = 2
        self.DOWN_2 = 3
        self.DELAY_2 = 4
        self.DOWN_3 = 5
        self.FINISHED = 6
        self.stage = self.IDLE

        self.timer = Timer()
        self.delay_1_start_time = 0.0
        self.delay_2_start_time = 0.0

        self.running = False

    def auto_descend(self):
        if self.stage == self.IDLE:
            self.stage = self.DOWN_1

        elif self.stage == self.DOWN_1:
            self.arm.desired_position = 17

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 8:
                self.stage = self.DELAY_1
                self.delay_1_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.DELAY_1:
            if self.delay_1_start_time + 0.5 < self.timer.getFPGATimestamp():
                self.stage = self.DOWN_2

        elif self.stage == self.DOWN_2:
            self.arm.desired_position = 5

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 4:
                self.stage = self.DELAY_2
                self.delay_2_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.DELAY_2:
            if self.delay_2_start_time + 0.5 < self.timer.getFPGATimestamp():
                self.stage = self.DOWN_3

        elif self.stage == self.DOWN_3:
            self.arm.desired_position = -10

            if abs(self.arm.get_arm_pitch() + 1) < 4:
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.running = False
