from subsystems.arm import Arm

class Amp:
    def _init__(self):
        # stages for Amping
        self.AMP_IDLE = 0
        self.ANGLE_ROBOT = 1
        self.AMP_SCAN = 2
        self.CENTER_ROBOT = 3
        self.DRIVING_ROBOT = 4
        self.MOVE_ARM = 5
        self.AMP_MOTOR_SPIN = 6
        self.RETURN_ARM = 7
        self.AMP_DONE = 8
        self.amp_stage = self.AMP_IDLE

    def angle_robot(self):
        """
        angle the robot pependicular with the wall.
        """
    def amp_scan(self):
        """
        if we get a raspi value return true
        else return false
        """
        pass

    def center_robot(self):
        """
        angle robot perpendicular 
        """
        pass
    def auto_shoot(self):
        if self.amp_stage == self.AMP_IDLE:
            self.amp_stage = self.ANGLE_ROBOT
        elif self.amp_stage == self.ANGLE_ROBOT:
            if self.angle_robot():
                self.amp_stage = self.AMP_SCAN
        elif self.amp_stage == self.AMP_SCAN:
            if self.amp_scan():
                self.amp_stage = self.CENTER_ROBOT
        elif self.amp_stage == self.CENTER_ROBOT:
            if self.center_robot():
                pass
