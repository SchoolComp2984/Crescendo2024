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

    def scan_for_april_tags(self):
        """
        get raspi april tag data
        if we find an april tag:
            return true
        else:
            return false
        """
        
        pass

    def turn_robot(self):
        """
        get current angle of robot from imu
        get needed angle through some apriltag data
        run PID
        move motors according to PID
        if new scan has same angles
            return true
        """
        pass

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
        """
        get data for arm angle from what is ideally another IMU on the arm
        if worst comes to worst, we have to use an encoder.
        MATH IT OUT! arctan ( (speaker height - arm height) / distance)
        return if we got a value (make it default like neg 1 see if it changed)
        """
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
    def spinning_shooter_motor(self):
        """
        spin the two shooting motors for a second
        when done spinning, return true.
        """
    def feed_note():
        """
        spin the motor on the intake
        when done return true
        note will have gone into shooter by now and will have been shot!
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

        elif self.shooter_stage == self.SHOOTER_MOTOR_SPIN:
            if self.spinning_shooter_motor():
                self.shooter_stage = self.FEED_NOTE

        elif self.shooter_stage == self.FEED_NOTE:
            if self.feed_note():
                self.shooter_stage = self.SHOOTER_DONE

        elif self.shooter_stage == self.SHOOTER_DONE:
            self.shooter_stage = self.SHOOTER_IDLE
