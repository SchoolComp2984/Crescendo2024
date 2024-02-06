#import math for arctan, wpilib for the timer
import math, wpilib

#import Shooter so we can spin the shooter motors
from subsystems.shooter import Shooter

#import IMU so we can use the imu on the arm
from subsystems.imu import IMU

#importing PID for various functions
from utils import pid

class Auto_Shoot:
    def __init__(self, _arm, _drive, _shooter, _intake):
        #different stages of shooting
        self.SHOOTER_IDLE = 0 #idle, not doing anyting
        self.ANGLE_SCAN = 1 #scan the apriltag on the speaker, get the angle that it is at
        self.ANGLE_ROBOT = 2 #angle the robot to center it on the tag
        self.DISTANCE_SCAN = 3 #scan the distance between the robot and the tag
        self.ARM_ANGLE_CALC = 4 #find the current angle of the arm, calculate needed angle for the arm
        self.ARM_ANGLE_MOVE = 5 #move the arm to the angle that we had calculated
        self.SHOOTER_MOTOR_SPIN = 6 #start spinning the shooter motors for about one second
        self.FEED_NOTE = 7 #feed the note into the shooter motors, firing the note
        self.RETURN_ARM = 8 #move the arm back down to the normal angle.
        self.SHOOTER_DONE = 9 #done with everything
        self.shooter_stage = self.SHOOTER_IDLE #set the current state to the idle state

        #reference to the arm that we passed in
        self.arm = _arm
        
        #reference to the drive that was passed in
        self.drive = _drive

        #reference to the shooter so we can use the shooter motors
        self.shooter = _shooter

        #reference to the intake so we can use the intake motors
        self.intake = _intake
        
        #initializing pid for shooter
        #zeroes are current placeholders that will be modified after tuning
        self.shooter_P = 0
        self.shooter_I = 0
        self.shooter_D = 0
        self.arm_val = 0
        self.shooter_pid = pid.PID(self.shooter_P, self.shooter_I, self.shooter_D, self.arm_val)

        #timer to track how long motors have been spinning and if we can move on to the next stage.
        self.timer = wpilib.Timer()
        self.shooter_spin_start_time = 0.0
        self.feeding_spin_start_time = 0.0

    #scans for the apriltag on the speaker so we can use the data values from it
    def scan_for_april_tags(self):
        """
        get raspi april tag data
        if we find an april tag:
            return true
        else:
            return false
        """
        
        pass

    #turns the robot to center it with the speaker apriltag.
    def turn_robot(self):
        #placeholder for the x of the apriltag from the raspi camera.
        #robot will turn until x is zero.
        april_tag_x = 10

        #if the x value is close enough to zero, return true
        # a bit of leeway should be fine.
        if abs(april_tag_x) < 3: return True

        #if the tag is to the right of the robot
        if april_tag_x > 0: 
            #should make the robot turn right by making the left wheels move forwards only.
            self.drive.tank_drive(.5, 0)

        #if the tag is to the left of the robot
        elif april_tag_x < 0:
            #should make the robot turn left by making only the right wheels move forwards
            self.drive.tank_drive(0, .5)

        #if the above if statement returning true isn't called, False is returned
        #basically if we're not in the right position, returns false to call the function again
        return False
    
    #raspi scans distance between bot and speaker(apriltag)
    def distance_scan(self):
        """
        get raspi april tag data
        if distance found:
            return true
        else 
            return false
        """
        pass

    def arm_angle_calc(self):
        #UNITS ARE IN INCHES
        #distance from raspi camera to apriltag
        #10 is a placeholder
        april_tag_distance = 100

        #height of the arm when shooting.
        arm_height = 18.5
        speaker_height = 80.7

        #our math formula for the angle that the arm needs to be set at ATAN = ARCTAN
        shooting_angle = math.atan((speaker_height - arm_height) / april_tag_distance)
        return True
    
    def arm_angle_move(self):
        """
        get values for our current arm angle 
        also get the value that we want to move the arm to
        this is where an imu would be really cool!
        run PID, move arm motors according to that
        if same angle:
            return true
        else:
            return false
        """

    #spins the shooter motor before for a second before we feed the note in.
    def spinning_shooter_motor(self):
        #starts spinning the shooter motors
        self.shooter.shooter_spin(1)

        #timer to check if it's been a second
        #if a second has passed, we return true
        if self.shooter_spin_start_time + 1 < self.timer.getFPGATimestamp(): return True
    
    def feed_note(self):
        #keeps the shooter motors spinning
        self.shooter.shooter_spin(1)

        #spins the intake motors to feed the note into the shooter motors
        self.intake.intake_spin(1)
        
        #if a second has passed, it will have most likely shot, so we can move on to the next step
        if self.feeding_spin_start_time + 1 < self.timer.getFPGATimestamp(): return True

    def return_arm():
        """
        move arm back to orignal position
        """
    def autonomous_shoot(self):
        if self.shooter_stage == self.SHOOTER_IDLE:
            self.shooter_stage = self.ANGLE_SCAN

        elif self.shooter_stage == self.ANGLE_SCAN:
            if self.scan_for_april_tags():
                self.shooter_stage = self.ANGLE_ROBOT

        elif self.shooter_stage == self.ANGLE_ROBOT:
            #turn the robot using the values of the apriltag scan
            if self.turn_robot():
                self.shooter_stage = self.DISTANCE_SCAN

        elif self.shooter_stage == self.DISTANCE_SCAN:
            if self.distance_scan():
                self.shooter_stage = self.ARM_ANGLE_CALC

        elif self.shooter_stage == self.ARM_ANGLE_CALC:
            if self.arm_angle_calc():
                self.shooter_stage = self.ARM_ANGLE_MOVE

        elif self.shooter_stage == self.ARM_ANGLE_MOVE:
            if self.arm_angle_move():
                self.shooter_stage = self.SHOOTER_MOTOR_SPIN
                self.shooter_spin_start_time = self.timer.getFPGATimestamp()

        elif self.shooter_stage == self.SHOOTER_MOTOR_SPIN:
            if self.spinning_shooter_motor():
                self.shooter_stage = self.FEED_NOTE
                self.feeding_spin_start_time = self.timer.getFPGATimestamp()

        elif self.shooter_stage == self.FEED_NOTE:
            if self.feed_note():
                self.shooter_stage = self.RETURN_ARM
        
        elif self.shooter_stage == self.RETURN_ARM:
            if self.return_arm():
                self.shooter_stage = self.SHOOTER_DONE

        elif self.shooter_stage == self.SHOOTER_DONE:
            self.shooter_stage = self.SHOOTER_IDLE
