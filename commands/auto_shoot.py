#import math for arctan, wpilib for the timer
import math, wpilib

class Auto_Shoot:
    def __init__(self, _arm, _drive, _shooter, _intake, _imu, _networking):
        #different stages of shooting
        self.IDLE = 0 #idle, not doing anyting
        self.CENTERING_ROBOT = 1 # move robot until apriltag is in center of screen
        self.ARM_TO_ANGLE = 2 
        self.SHOOTER_MOTOR_SPIN = 3 #start spinning the shooter motors for about 1.5-1.75 seconds
        self.FEED_NOTE = 4 #feed the note into the shooter motors, firing the note
        self.RETURN_ARM = 5 # move the arm back to position inside the robot
        self.FINISHED = 6 #done with everything
        self.shooter_stage = self.SHOOTER_IDLE #set the current state to the idle state

        #reference to the arm that we passed in
        self.arm = _arm
        
        #reference to the drive that was passed in
        self.drive = _drive

        #reference to the shooter so we can use the shooter motors
        self.shooter = _shooter

        #reference to the intake so we can use the intake motors
        self.intake = _intake

        #reference to the imu
        self.imu = _imu

        #reference to networking
        self.networking = _networking
        
        #timer to track how long motors have been spinning and if we can move on to the next stage.
        self.timer = wpilib.Timer()
        self.shooter_spin_start_time = 0.0
        self.feeding_spin_start_time = 0.0

    def autonomous_shoot(self):
        if self.shooter_stage == self.IDLE:
            self.shooter_stage = self.CENTERING_ROBOT

        elif self.shooter_stage == self.CENTERING_ROBOT:
            # get position of april tag (x)
            # if the apriltag x position is negative, rotate robot left
            # else if april tag position is positive, rotate robot right
            # if it is within tolerance band, move to next stage
                
            self.shooter_stage = self.ARM_TO_ANGLE
    
        elif self.shooter_stage == self.ARM_TO_ANGLE:
            # get distance of apriltag
            # convert to same units as all other numbers
            # calculate arm height
            # run arctan calculation to get angle
            # justify for angle of shooter relative to arm
            # move arm to the angle
            # once arm is within a certain degree of tolerance, move to next step OR after certain amount of time if tolerance if not consistent
            # set holding position and everything
            
            self.shooter_stage = self.SHOOTER_MOTOR_SPIN

        elif self.shooter_stage == self.SHOTER_MOTOR_SPIN:
            # spin shooter motor for 1.5 seconds
            # if 1.5 seconds is up, move to feeding
            
            self.shooter_stage = self.FEED_NOTE

        elif self.shooter_stage == self.FEED_NOTE:
            # spin shooter and intake for 1.5 seconds
            # if 1.5 seconds is up, move to returning arm
            
            self.shooter_stage = self.RETURN_ARM:

        elif self.shooter_stage == self.RETURN_ARM:
            # move arm to position that is in the chassis
            # if within tolerance OR timer, move to finished
            
            self.shooter_stage = self.FINISHED

        elif self.shooter_stage == self.FINISHED:
            # reset
            # alert driver ready to start sequence again
            # go to idle ?
            
            pass
