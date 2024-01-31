from subsystems.shooter import Shooter
from subsystems.arm import Arm

class Shoot:
    def __init__(self):
        #different stages of shooting
        self.SHOOTER_IDLE = 0 #idle, not doing anyting
        self.ANGLE_SCAN = 1 #scan the apriltag on the speaker, get the angle that it is at
        self.ANGLE_ROBOT = 2 #angle the robot to center it on the tag
        self.DISTANCE_SCAN = 3 #scan the distance between the robot and the tag
        self.ARM_ANGLE_CALC = 4 #find the current angle of the arm, calculate needed angle for the arm
        self.ARM_ANGLE_MOVE = 5 #move the arm to the angle that we had calculated
        self.SHOOTER_MOTOR_SPIN = 6 #start spinning the shooter motors for about one second
        self.FEED_NOTE = 7 #feed the note into the shooter motors, firing the note
        self.SHOOTER_DONE = 8 #done with everything
        self.shooter_stage = self.SHOOTER_IDLE #set the current state to the idle state

    def scan_for_april_tags():
        """
        get raspi april tag data
        if we find an april tag:
            return true
        else:
            return false
        """
        
        pass

    def turn_robot(self, current_angle, desired_angle):
        """
        get current angle
        get needed angle
        run PID
        move motors according to PID
        if new scan has same angles
            return true
        """
        self.current_angle = current_angle
        self.desired_angle = desired_angle


        pass

    def distance_scan():
        """
        get raspi april tag data
        if distance found:
            return true
        else return false
        """
        pass

    def arm_angle_calc():
        """
        return angle of arm currently
        gyroscope on arm?
        or count revs
        how we do this I have no clue
        """

    def autonomous_shoot(self):
        if self.shooter_stage == self.SHOOTER_IDLE:
            self.shooter_stage = self.ANGLE_SCAN
        elif self.shooter_stage == self.ANGLE_SCAN:
            if self.scan_for_april_tags():
                self.shooter_stage = self.ANGLE_ROBOT
        elif self.shooter_stage == self.ANGLE_ROBOT:
            #turn the robot using the values of the apriltag scan
            #if turn_robot(current IMU, current IMU + bearing):
                self.shooter_stage = self.DISTANCE_SCAN
        elif self.shooter_stage == self.DISTANCE_SCAN:
            if self.distance_scan():
                self.shooter_stage = self.ARM_ANGLE_CALC
        elif self.shooter_stage == self.ARM_ANGLE_CALC:
            #if we get an arm angle, we go onto the next stage    
            pass