from subsystems.arm import Arm

class AutoAmp:
    def _init__(self):
        # stages for using the amp.
        #iterating through these stages with a tracker that will move on to the next stage after the current one is finished.
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
        #angles the robot perpendicularly with the wall so that the back is facing directly at the amp.
        #aligns us fully and all we have to do is then to move left or right.
        #IMPORTANT - DEPENDING ON WHETHER WE ARE RED OR BLUE, THE ANGLE THAT WE TURN WILL CHANGE.
        """
        if red team:
            turn 90 degrees to the left
        else:
            turn 90 degrees to the right
            likely the use of PIDS for turning.
        """
    def amp_scan(self):
        #scanning the apriltag on the amp.
        #looking for coordinates that we can use to allign ourselves with to be squarely in front of the amp.
        """
        if we get a raspi value return true
        else return false
        """
        pass

    def center_robot(self):
        #center the robot with the amp.
        """
        if left of amp:
            move right a certain amount
        if right of amp:
            move left a certain amount
        pids for moving? likely
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
        #move the arm to the right angle to drop the note directly into the amp.
        #arm will be facing downwards
        #yaw on the arm should be its angle.
        """
        get current arm yaw
        get desired arm yaw
        pass the error into the function in the arm
        """
        #Arm.move_arm_to_angle(curr_yaw, desired_yaw)
        pass

    def amp_motor_spin(self):
        #slowly spin the motors for both the intake and the shooting motors.
        #won't be at as fast as a speed as shooting.
        """
        spin intake motors
        spin shooting motors
        """
        pass

    def return_arm(self):
        #return the arm to the original position
        """
        get current arm yaw
        """
        #Arm.move_arm_to_angle(curr_yaw, desired_yaw)
    def autonomous_amp(self):

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
