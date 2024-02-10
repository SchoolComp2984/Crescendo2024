# import necessary libraries
# wpilib contains useful classes and methods for interfacing with parts of our robot such as sensors and even the driver station
import wpilib

# phoenix5 contains classes and methods to inferface with motors distributed by cross the road electronics
# third party library
import phoenix5

#importing rev libraries for our neo motors
import rev

#import our Autonomous
from commands.autonomous import Autonomous

#import our shooting
from commands.auto_shoot import Shoot

#import our amp 
from commands.auto_amp import AutoAmp

# import our Drive class that contains various modes of driving and methods for interfacing with our motors
from subsystems.drive import Drive

#import our Shooter class
from subsystems.shooter import Shooter

#import our intake class
from subsystems.intake import Intake

#import our climb class
from subsystems.climber import Climb

# import our IMU wrapper class with methods to access different values the IMU provides
from subsystems.imu import IMU

# import our interpolation function used for joysticks
from utils.math_functions import interpolation_drive

#import our PID function
from utils.pid import PID

# import our constants which serve as "settings" for our robot/code
# mainly IDs for CAN motors, sensors, and our controllers
from utils import constants

# create our base robot class
class MyRobot(wpilib.TimedRobot):
    # initialize timers, motors, and sensors
    # create reference to physical parts of the robot
    def robotInit(self):
        # create an instance of the wpilib.Timer class
        # used for autotonous capabilities
        # for example, because we have a timer, we can move the robot forwards for x amount of seconds
        self.timer = wpilib.Timer()

        # create reference to our Falcon 500 motors
        # each Falcon 500 has a Talon FX motor controller
        # we need to provide each instance of the Talon FX class with its corresponding CAN ID
        # we configured the IDs using the Phoenix Tuner
        self.front_right = phoenix5._ctre.WPI_TalonFX(constants.FRONT_RIGHT_ID)
        self.front_left = phoenix5._ctre.WPI_TalonFX(constants.FRONT_LEFT_ID)
        self.back_left = phoenix5._ctre.WPI_TalonFX(constants.BACK_LEFT_ID)
        self.back_right = phoenix5._ctre.WPI_TalonFX(constants.BACK_RIGHT_ID)

        # invert the motors on the right side of our robot
        self.front_right.setInverted(True)
        self.back_right.setInverted(True)


        #create reference to our Neo motors
        self.shooter_upper_motor = rev.CANSparkMax(constants.SHOOTER_UPPER_MOTOR_ID, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.shooter_lower_motor = rev.CANSparkMax(constants.SHOOTER_LOWER_MOTOR_ID, rev.CANSparkLowLevel.MotorType.kBrushless)

        # create reference to our intake motor
        self.intake_motor = rev.CANSparkMax(constants.INTAKE_MOTOR_ID, rev.CANSparkLowLevel.MotorType.kBrushless)

        #create reference to our climb motors (Falcon 500)
        #self.climb_motor_left = phoenix5._ctre.WPI_TalonFX(constants.CLIMB_LEFT_ID)
        #self.climb_motor_right = phoenix5._ctre.WPI_TalonFX(constants.CLIMB_RIGHT_ID)

        # create a reference to our IMU
        self.imu_motor_controller = phoenix5._ctre.WPI_TalonSRX(constants.IMU_ID)
        self.imu = IMU(self.imu_motor_controller)

        #reference to the two arm motors that move it up and down
        self.arm_motor_left = rev.CANSparkMax(constants.ARM_LEFT_ID, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.arm_motor_right = rev.CANSparkMax(constants.ARM_RIGHT_ID, rev.CANSparkLowLevel.MotorType.kBrushless)

        # create an instance of our controller
        # it is an xbox controller at id constants.CONTROLLER_ID, which is 0
        self.controller = wpilib.XboxController(constants.CONTROLLER_ID)

        # create an instance of our Drive class that contains methods for different modes of driving
        self.drive = Drive(self.front_right, self.front_left, self.back_left, self.back_right, self.imu)
        
        #create an instance of our shooting function
        self.shooter = Shooter(self.shooter_lower_motor, self.shooter_upper_motor)

        #create an instance of our Intake class that contains methods for shooting
        self.intake = Intake(self.intake_motor)

        #create an instance of our amping function
        #self.auto_amp = AutoAmp(self.shooter_motor)

        #create an instance of our Climb class that contains methods for climbing
        #self.climb = Climb(self.climb_motor_left, self.climb_motor_right)

        # variable for what mode of drive we are in
        # toggle between 0 and whatever max number we want to set it to
        self.drive_mode_toggle = 0

    # setup before our robot transitions to autonomous
    def autonomousInit(self):
        pass

    # ran every 20 ms during autonomous mode
    def autonomousPeriodic(self):
        pass

    # setup before our robot transitions to teleop (where we control with a joystick or custom controller)
    def teleopInit(self):
        pass
        
    # ran every 20 ms during teleop
    def teleopPeriodic(self):
        # test our intake and shooter 2/8 meeting
        if self.controller.getAButton():
            self.intake.intake_spin(1)

        elif self.controller.getBButton():
            self.shooter.shooter_spin(0.7)

        else:
            self.intake.stop()
            self.shooter.stop()


        # get the x and y axis of the left joystick on our controller
        joystick_x = self.controller.getLeftX()

        # rember that y joystick is inverted
        # multiply by -1
        # "up" on the joystick is -1 and "down" is 1
        joystick_y = self.controller.getLeftY() * -1

        # get the x axis of the right joystick used for turning the robot in place
        joystick_turning = self.controller.getRightX()

        #Calling the method for the drive mode with a toggle that will switch between driving modes
        if self.controller.getAButton(): self.drive_mode_toggle = 0
        elif self.controller.getBButton(): self.drive_mode_toggle = 1
        elif self.controller.getYButton(): self.drive_mode_toggle = 2

        #Driving modes that will spin the motors
        #We pass in the joystick values for the drive controls
        
        if self.drive_mode_toggle == 0:
            #if the A button is pressed, we are in robot oriented drive
            self.drive.field_oriented_drive(joystick_x, joystick_y, joystick_turning)
            if self.controller.getBackButton():
                self.imu.reset_yaw()

        elif self.drive_mode_toggle == 1:
            #if the B button is pressed, we go into Evan's drive
            self.drive.evans_drive(joystick_x, joystick_y)
            
        elif self.drive_mode_toggle == 2:
            #if the Y button is pressed, we go into field oriented drive
            self.drive.mecanum_drive_robot_oriented(joystick_x, joystick_y, joystick_turning)

        #if the left bumper is pressed, we shoot.
        #if self.controller.getLeftBumperPressed(): self.shoot.autonomous_shoot()
        
        #if the right bumber is pressed, we do the amp
        #if self.controller.getRightBumperPressed(): self.auto_amp.autonomous_amp()

        # print out the joystick values
        # mainly used for debugging where we realized the y axis on the lefy joystick was inverted
        #print(f"getLeftX: {self.controller.getLeftX()}, getLeftY: {self.controller.getLeftY()}, getRightX: {self.controller.getRightX()}, getRightY: {self.controller.getRightY()}")
        
        # print out the left and right triggers to see if they are pressed
        #print(f"left trigger: {self.controller.getLeftTriggerAxis()}, right trigger: {self.controller.getRightTriggerAxis()}")

# run our robot code
if __name__ == "__main__":
    wpilib.run(MyRobot)

# the command that deploys our code to our robot:
# py -3 -m robotpy deploy