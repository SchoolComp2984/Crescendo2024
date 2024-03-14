#import math for arctan, wpilib for the timer
import math, wpilib

class AutoShoot:
    def __init__(self, _arm, _drive, _shooter, _intake, _imu, _networking):
        #different stages of shooting
        self.IDLE = 0 #idle, not doing anyting
        self.CENTERING_ROBOT = 1 # move robot until apriltag is in center of screen
        self.ARM_TO_ANGLE = 2 
        self.SHOOTER_MOTOR_SPIN = 3 #start spinning the shooter motors for about 1.5-1.75 seconds
        self.FEED_NOTE = 4 #feed the note into the shooter motors, firing the note
        self.RETURN_ARM = 5 # move the arm back to position inside the robot
        self.FINISHED = 6 #done with everything
        self.stage = self.IDLE #set the current state to the idle state

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

        # initialize shooter and intake spin start times
        self.shooter_spin_start_time = 0.0
        self.feeding_spin_start_time = 0.0

    def auto_shoot(self):
        if self.stage == self.IDLE:
            # check if ready, move to centering robot stage
            self.stage = self.CENTERING_ROBOT

        elif self.stage == self.CENTERING_ROBOT:
            # get the april tag position from the raspberry pi
            apriltag_x = self.networking.get_april_tag_data()[0]

            print(f"apriltag position: {apriltag_x}")

            if apriltag_x is None:
                return

            # if april tag is left of center, rotate left
            if apriltag_x < -5:
                self.drive.tank_drive(-0.1, 0.1)

            # if april tag is right of center, rotate right
            elif apriltag_x > 5:
                self.drive.tank_drive(0.1, -0.1)
                
            # else (meaning we are somewhere in the middle), move to angling the arm
            else:
                self.stage = self.ARM_TO_ANGLE
    
        elif self.stage == self.ARM_TO_ANGLE:
            # get distance of apriltag
            apriltag_distance = self.networking.get_april_tag_data()[2]

            # height of speaker
            speaker_height = 2

            # height of robot arm
            arm_height = 0.265

            # find total height
            height = speaker_height - arm_height
            
            # run arctan calculation to get angle
            arm_angle = math.atan2(height / apriltag_distance)

            # justify for angle of shooter relative to arm
            justified_arm_angle = arm_angle - 57
            
            # move arm to the angle
            self.arm.desired_angle = justified_arm_angle

            # once arm is within a certain degree of tolerance, move to next step OR after certain amount of time if tolerance if not consistent
            if abs(self.arm.get_arm_pitch() - self.arm.desired_arm_angle) < 4:
                self.stage = self.SHOOTER_MOTOR_SPIN
                self.shooter_spin_start_time = self.timer.getFPGATimestamp()
                
                # shooting override to hold arm in place
                self.arm.shooting_override = True
            
        elif self.stage == self.SHOOTER_MOTOR_SPIN:
            # spin shooter motor for 1.5 seconds
            self.shooter.shooter_spin(1)

            # if 1.5 seconds is up, move to feeding
            if self.shooter_spin_start_time + 1.75 < self.timer.getFPGATimestamp():
                self.stage = self.FEED_NOTE
                self.feeding_spin_start_time = self.timer.getFPGATimestamp()
            
            
        elif self.stage == self.FEED_NOTE:
            # spin shooter and intake
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)
            
            # if 1.5 seconds is up, move to returning arm
            if self.feeding_spin_start_time == self.timer.getFPGATimestamp():
                self.stage = self.RETURN_ARM

        elif self.stage == self.RETURN_ARM:
            # move arm to position that is in the chassis
            self.arm.desired_position = 60

            # if within tolerance OR timer, move to finished
            if abs(self.arm.get_pitch() - self.arm.desired_arm_angle) < 4:
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.arm.shooting_override = False
            self.running = False



    def auto_shoot_interpolated(self):
        pass

        # CALIBRATION:
        # get move the robot to a known distance from the speaker
        # find the angle the arm is at so that it can accurately shoot into the speaker from that distance
        # put that data into a 2d array with each element in format [distance, angle]
        # repeat until we are at a distance where we can not longer reliably see the apriltag

        # check in IDLE if we can see an apriltag
        # move so that it is centered
        # get distance from apriltag
        # interpolate between angles in the array to find what should be a correct angle for our arm
        # move arm to that angle
        # set holding arm power and override
        # rev shooter motors
        # feed the note from intake to shooter
        # move the arm to the position we want it to be at after shooting
        # done sequence
    
    
