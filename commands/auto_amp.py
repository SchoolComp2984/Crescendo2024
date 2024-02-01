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

    def drive_robot(self):
        """
        all we need to do is drive the robot down in front of the amp basically
        probably just run the drive
        when we are finally close enough to the amp, return true
        else return false
        """
        pass

    def move_arm(self):
        """
        move the arm from the current intake position to the angle
        needed for the note to drop into the amplifier
        probably do some testing for this and the optimal angle.
        """
        pass

    def amp_motor_spin(self):
        """
        spin the intake motors a bit first
        then spin the shooter motors but at a lower speed enough to make 
        the note fall out
        """
        pass

    def return_arm(self):
        """
        return arm back to intake position.
        """
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
                self.amp_stage = self.DRIVING_ROBOT

        elif self.amp_stage == self.DRIVING_ROBOT:
            if self.drive_robot():
                self.amp_stage == self.MOVE_ARM

        elif self.amp_stage == self.MOVE_ARM:
            if self.move_arm():
                self.amp_stage == self.AMP_MOTOR_SPIN

        elif self.amp_stage == self.AMP_MOTOR_SPIN:
            if self.amp_motor_spin():
                self.amp_stage = self.RETURN_ARM

        elif self.amp_stage == self.RETURN_ARM:
            if self.return_arm():
                self.amp_stage = self.AMP_DONE
                
        elif self.amp_stage == self.AMP_DONE:
            self.amp_stage = self.AMP_IDLE
