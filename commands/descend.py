from wpilib import Timer

from subsystems.arm import Arm

class Descend:
    def __init__(self, _arm : Arm):
        self.arm = _arm

        self.IDLE = 0
        self.TIPPING = 1
        self.DOWN = 2
        self.FINISHED = 3
        self.stage = self.IDLE

        self.timer = Timer()
        self.tipping_start_time = 0.0
        
        self.descending = False

    def descend(self):
        if self.stage == self.IDLE:
            if self.arm.get_arm_pitch() >= 70:
                self.stage = self.TIPPING
                self.tipping_start_time = self.timer.getFPGATimestamp()
            else:
                self.stage = self.DOWN

        elif self.stage == self.TIPPING:
            if self.arm.get_arm_pitch() > 80:
                self.arm.set_speed(-0.05)
            else:
                self.arm.set_speed(-0.03)
            
            if self.arm.get_arm_pitch() <= 60:
                self.stage = self.DOWN

        elif self.stage == self.DOWN:
            if self.arm.get_arm_pitch() > 5:
                self.arm.set_speed(0.05)
            
            else:
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.arm.desired_position = -15
            self.descending = False
            self.stage = self.IDLE
