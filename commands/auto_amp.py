#importing the arm so we can use the functions to move the arm up and down.
from subsystems.arm import Arm

#import intake so we can spin the intake motors to feed the note into the shooter motor
from subsystems.intake import intake
#import shooter so we can spin the shooter motors to move the note out
from subsystems.shooter import Shoot

# import driver station to get the alliance color that we're on.
from wpilib import DriverStation

class Auto_Amp:
    def _init__(self, _arm, _drive, _shooter, _intake, _imu):
        # stages for using the amp.
        #iterating through these stages with a tracker that will move on to the next stage after the current one is finished.
        self.AMP_IDLE = 0
        self.ANGLE_ROBOT = 1
        self.MOVE_ARM = 2
        self.AMP_MOTOR_SPIN = 3
        self.RETURN_ARM = 4
        self.AMP_DONE = 5
        self.amp_stage = self.AMP_IDLE

        # create a reference to our driver station
        self.driver_station = DriverStation

        #reference to the arm
        self.arm = _arm

        #reference to the drive
        self.drive = _drive

        #reference to the shooter
        self.shooter = _shooter
        
        #reference to the intake
        self.intake = _intake

        self.imu = _imu

    def angle_robot(self):
        #angles the robot perpendicularly with the wall so that the back is facing directly at the amp.
        #aligns us fully and all we have to do is then to move left or right.
        #IMPORTANT - DEPENDING ON WHETHER WE ARE RED OR BLUE, THE ANGLE THAT WE TURN WILL CHANGE.
        #NEEDS WORK
        alliance_color = self.driver_station.getAlliance()
        if alliance_color.value() == DriverStation.Alliance.kRed:
            #if red, turn left 90 degrees
            self.drive.set_robot_to_angle(270)
        elif alliance_color.value() == DriverStation.Alliance.kBlue:
            self.drive.set_robot_to_angle(90)
            
    def move_arm(self):
        current_angle = self.imu.get_yaw()
        desired_angle = 90 #90 is a placeholder for now, but we can jus
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
