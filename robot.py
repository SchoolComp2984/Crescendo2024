# import necessary libraries
# wpilib contains useful classes and methods for interfacing with parts of our robot such as sensors and even the driver station
import wpilib

# phoenix5 contains classes and methods to inferface with motors distributed by cross the road electronics
# third party library
import phoenix5

#importing rev libraries for our neo motors
import rev

# import our Drive class that contains various modes of driving and methods for interfacing with our motors
from subsystems.drive import Drive

#import our Shooter class
from subsystems.shooter import Shooter

#import our intake class
from subsystems.intake import Intake

#import our climb class
from subsystems.climb import Climb

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
        self.shooter_motor = rev.CANSparkMax(constants.SHOOTER_MOTOR_ID)
        self.intake_motor = rev.CANSparkMax(constants.INTAKE_MOTOR_ID)

        #create reference to our climb motors (Falcon 500)
        self.climb_motor_left = phoenix5._ctre.WPI_TalonFX(constants.CLIMB_LEFT_ID)
        self.climb_motor_right = phoenix5._ctre.WPI_TalonFX(constants.CLIMB_RIGHT_ID)

        # create a reference to our IMU
        self.imu_motor_controller = phoenix5._ctre.WPI_TalonSRX(constants.IMU_ID)
        self.imu = IMU(self.imu_motor_controller)

        # create an instance of our controller
        # it is an xbox controller at id constants.CONTROLLER_ID, which is 0
        self.controller = wpilib.XboxController(constants.CONTROLLER_ID)

        # create an instance of our Drive class that contains methods for different modes of driving
        self.drive = Drive(self.front_right, self.front_left, self.back_left, self.back_right, self.imu)
        
        #create an instance of our Shooter class that contains methods for shooting
        self.shoot = Shooter(self.shooter_motor)

        #create an instance of our Intake class that contains methods for shooting
        self.intake = Intake(self.intake_motor)

        #create an instance of our Climb class that contains methods for climbing
        self.climb = Climb(self.climb_motor_left, self.climb_motor_right)

        # variable for what mode of drive we are in
        # toggle between 0 and whatever max number we want to set it to
        self.drive_mode_toggle = 0

        # set the maximum value of our drive modes we can toggle between
        self.drive_mode_toggle_max = 1

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
        # get the x and y axis of the left joystick on our controller
        joystick_x = self.controller.getLeftX()

        # rember that y joystick is inverted
        # multiply by -1
        # "up" on the joystick is -1 and "down" is 1
        joystick_y = self.controller.getLeftY() * -1

        # get the x axis of the right joystick used for turning the robot in place
        joystick_turning = self.controller.getRightX()

        #Calling the method for the drive mode with a toggle that will switch between driving modes
        #if the start button is pressed
        if self.controller.getStartButton():
            #set the variable to 0 if it is currently at the max value
           if self.drive_mode_toggle == self.drive_mode_toggle_max: self.drive_mode_toggle = 0
           #if not at the max value, we add one to the variable which will bring us to the next mode
           else: self.drive_mode_toggle +=1

        #Driving modes that will spin the motors
        #We pass in the joystick values for the drive controls
        if self.drive_mode_toggle == 0:
            #if the toggle is at zero, we are in mecanum drive mode
            self.drive.mecanum_drive_robot_oriented(joystick_x, joystick_y, joystick_turning)
        elif self.drive_mode_toggle == 1:
            #if the toggle is at one, we are in arcade drive
            self.drive.evans_drive(joystick_x, joystick_y)

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