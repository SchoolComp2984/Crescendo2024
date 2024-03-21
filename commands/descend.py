from wpilib import Timer

from subsystems.arm import Arm

class Descend:
    def __init__(self, _arm : Arm):
        self.arm = _arm

        self.IDLE = 0
        self.DOWN_1 = 1
        self.DELAY_1 = 2
        self.DOWN_2 = 3
        self.FINISHED = 6
        self.stage = self.IDLE

        self.timer = Timer()
        self.delay_1_start_time = 0.0

        self.descending = False

    def auto_descend(self):
        if self.stage == self.IDLE:
            self.stage = self.DOWN_1
            #print("exiting idle")

        elif self.stage == self.DOWN_1:
            self.arm.desired_position = 10
            #print("moving to 15")

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 8:
                #print("within 8 degrees from 15, moving to delay")
                self.delay_1_start_time = self.timer.getFPGATimestamp()
                self.stage = self.DELAY_1


        elif self.stage == self.DELAY_1:
            #print("starting delay")
            if self.delay_1_start_time + 0.5 < self.timer.getFPGATimestamp():
                self.stage = self.DOWN_2
                #print("done delay")

        elif self.stage == self.DOWN_2:
            #print("moving down to -10")
            self.arm.desired_position = -10

            if abs(self.arm.get_arm_pitch()) < 4:
                #print("within 4 degrees from 0")
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            #print("finished")
            self.stage = self.IDLE
            self.descending = False