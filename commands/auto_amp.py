
class AutoAmp:
    def __init__(self, _arm, _drive, _shooter, _intake, _imu, _networking):
        # stages for using the amp.
        #iterating through these stages with a tracker that will move on to the next stage after the current one is finished.
        self.AMP_IDLE = 0
        self.ANGLE_ROBOT = 1
        self.MOVE_ARM = 2
        self.AMP_MOTOR_SPIN = 3
        self.RETURN_ARM = 4
        self.AMP_DONE = 5
        self.amp_stage = self.AMP_IDLE

        #reference to the arm
        self.arm = _arm

        #reference to the drive
        self.drive = _drive

        #reference to the shooter
        self.shooter = _shooter
        
        #reference to the intake
        self.intake = _intake

        #referencing imu
        self.imu = _imu

        #referencing networking
        self.networking = _networking

        #intermediate variable for apriltag data
        self.apriltag_data = None

    def angle_robot(self):
        #angles the robot perpendicularly with the wall so that the back is facing directly at the amp.
        #aligns us fully and all we have to do is then to move left or right.
        #IMPORTANT - DEPENDING ON WHETHER WE ARE RED OR BLUE, THE ANGLE THAT WE TURN WILL CHANGE.
        #NEEDS WORK
        #gets the alliance color through driver station data
        
        #get apriltag data and put into an array
        self.apriltag_data = self.networking.get_apriltag_data()

        #get X value of apriltag
        self.apriltag_x = self.apriltag_data[0]

        #if the X value is close enough to the center, we're good.
        if abs(self.apriltag_x) < 10: return True

        #x value on left, move right
        elif(self.apriltag_x) < -10:
            self.drive.mecanum_drive_robot_oriented(0, .5, 0)
        #x value on right, move left
        elif self.apriltag_x > 10:
            self.drive.mecanum_drive_robot_oriented(0, -.5, 0)
        #the camera is gonna be facing backwards so the directions are swapped.
        #if the apriltag is on the right side of the camera, it is in reality on the left of our robot, and vice-versa

    def move_arm(self):
        """
        get current arm yaw
        get desired arm yaw
        pass the error into the function in the arm
        """
        #Arm.move_arm_to_angle(curr_yaw, desired_yaw)
        pass

    def amp_motor_spin(self):
        #spin both motors but slower.
        self.intake.intake_spin(.3)
        self.shooter.shooter_spin(.5)
        
        pass

    def return_arm(self):
        #return the arm to the original position
        """
        get current arm yaw
        """
        #Arm.move_arm_to_angle(curr_yaw, desired_yaw)
    def autonomous_amp(self):
        #status tracker that goes through all the different steps of amping
        if self.amp_stage == self.AMP_IDLE:
            self.amp_stage = self.ANGLE_ROBOT

        elif self.amp_stage == self.ANGLE_ROBOT:
            if self.angle_robot():
                self.amp_stage = self.MOVE_ARM
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
