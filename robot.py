# import necessary libraries
# wpilib contains useful classes and methods for interfacing with parts of our robot such as sensors and even the driver station
import wpilib

# import cscore for pov camera
from cscore import CameraServer

# phoenix5 contains classes and methods to inferface with motors distributed by cross the road electronics
# third party library
import phoenix5

#importing rev libraries for our neo motors
import rev

#IMPORTING OUR COMMANDS
#import our Autonomous
from commands.autonomous import Autonomous

#import our shooting
from commands.auto_shoot import Auto_Shoot

# import our auto shooting tested on 3/6 meeting
from commands.auto_shoot_test import AutoShoot

#import our amp 
from commands.auto_amp import Auto_Amp

#import our intake
from commands.auto_intake import Auto_Intake

#IMPORTING OUR SUBSYSTEMS
# import our Drive class that contains various modes of driving and methods for interfacing with our motors
from subsystems.drive import Drive

#import our Shooter class
from subsystems.shooter import Shooter

#import our networking
from subsystems.networking import NetworkReciever

#import our intake class
from subsystems.intake import Intake

from subsystems.arm import Arm

# import our IMU wrapper class with methods to access different values the IMU provides
from subsystems.imu import IMU

#IMPORTING UTILITIES

#import our PID function
from utils.pid import PID

# import clamp function
from utils.math_functions import clamp

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

        # init camera
        #CameraServer.startAutomaticCapture()

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

        #create reference to our Falcon motors
        self.shooter_upper_motor = phoenix5._ctre.WPI_TalonFX(constants.SHOOTER_UPPER_MOTOR_ID)
        self.shooter_lower_motor = phoenix5._ctre.WPI_TalonFX(constants.SHOOTER_LOWER_MOTOR_ID)

        self.shooter_upper_motor.setInverted(True)
        self.shooter_lower_motor.setInverted(True)

        # create reference to our intake motor
        self.intake_motor = rev.CANSparkMax(constants.INTAKE_MOTOR_ID, rev.CANSparkLowLevel.MotorType.kBrushless)

        # create a reference to our IMU
        self.imu_motor_controller = phoenix5._ctre.WPI_TalonSRX(constants.IMU_ID)
        self.imu = IMU(self.imu_motor_controller)

        #reference to the two arm motors that move it up and down
        self.arm_motor_left_front = rev.CANSparkMax(constants.ARM_LEFT_FRONT_ID, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.arm_motor_left_back = rev.CANSparkMax(constants.ARM_LEFT_BACK_ID, rev.CANSparkLowLevel.MotorType.kBrushless)
        
        self.arm_motor_right_front = rev.CANSparkMax(constants.ARM_RIGHT_FRONT_ID, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.arm_motor_right_back = rev.CANSparkMax(constants.ARM_RIGHT_BACK_ID, rev.CANSparkLowLevel.MotorType.kBrushless)

        # invert left side motors
        self.arm_motor_left_front.setInverted(True)
        self.arm_motor_left_back.setInverted(True)


        # reference to our arm IMU
        self.arm_imu_motor_controller = phoenix5._ctre.WPI_TalonSRX(constants.ARM_IMU_ID)
        self.arm_imu = IMU(self.arm_imu_motor_controller)

        #REFERENCES/INSTANCES OF THE SUBSYSTEMS
        #instance of the arm class that has methods for moving the arm
        self.arm = Arm(self.arm_motor_left_front, self.arm_motor_left_back, self.arm_motor_right_front, self.arm_motor_right_back, self.arm_imu)

        #create an instance of our Intake class that contains methods for shooting
        self.intake = Intake(self.intake_motor)

        # create an instance of our Drive class that contains methods for different modes of driving
        self.drive = Drive(self.front_right, self.front_left, self.back_left, self.back_right, self.imu)

        self.networking = NetworkReciever()
        
        #create an instance of our shooter
        self.shooter = Shooter(self.shooter_lower_motor, self.shooter_upper_motor)

        # create an instance of our controller
        # it is an xbox controller at id constants.CONTROLLER_ID, which is 0
        self.controller = wpilib.XboxController(constants.CONTROLLER_ID)

        #create an instance of our amping function
        self.auto_amp = Auto_Amp(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)

        #create an instance for the auto shoot
        #self.auto_shoot = Auto_Shoot(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)

        # create instance of auto shoot class
        self.auto_shoot_test = AutoShoot(self.intake, self.shooter)

        #instance for the auto intake
        self.auto_intake = Auto_Intake(self.arm, self.drive, self.intake, self.imu, self.networking)

        # override variables  to prevent spinning the same motors in multiple places in the code
        self.drive_override = True
        self.intake_override = True
        self.shoot_override = True
        self.arm_override = True


        if self.arm_imu.is_ready(): print("arm_imu is in fact ready")
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

        #CODE FOR TESTING THE ARM
        if not self.arm_override:
            # arm all the way down = -82 deg ~use -80 deg
            # arm amp postion (perp to all the way down) = -7 deg

            #print(f"arm angle: {self.arm.get_arm_pitch()}")
            
            if self.controller.getAButton():
                self.arm.shooting_override = False
                self.arm.desired_position = 40
            elif self.controller.getYButton():
                self.arm.shooting_override = False
                self.arm.desired_position = -11
            
            self.arm.arm_to_angle(self.arm.desired_position)


        #INTAKE AND SHOOTER TESTING
        """
        if not self.intake_shoot_override:
            if self.controller.getXButton():
                self.intake.intake_spin(1)
            else:
                self.intake.stop()

            if self.controller.getYButton():
                self.shooter.shooter_spin(1)
            else:
                self.shooter.stop()
        """

        if not self.intake_override:
            if self.controller.getRightBumper():
                self.intake.intake_spin(1)
            elif self.controller.getLeftBumper():
                self.intake.intake_spin(-1)
            else:
                self.intake.stop()

        if not self.shoot_override:
            if self.controller.getBButton():
                self.arm.shooting_override = True
                self.auto_shoot_test.auto_shoot()
            else:
                self.shooter.stop()


 
                
        #WORKING DRIVE CODE
        # check if our drive is not overriden - we are not doing some autonomous task and in this case just want to drive around
        if not self.drive_override:
            # get the x and y axis of the left joystick on our controller
            joystick_x = self.controller.getLeftX()

            # rember that y joystick is inverted
            # multiply by -1;
            # "up" on the joystick is -1 and "down" is 1
            joystick_y = self.controller.getLeftY() * -1

            # get the x axis of the right joystick used for turning the robot in place
            joystick_turning = self.controller.getRightX()

            # run field oriented drive based on joystick values
            self.drive.field_oriented_drive(joystick_x, joystick_y, joystick_turning)
            
            # if we click the back button on our controller, reset the "zero" position on the yaw to our current angle
            if self.controller.getBackButton():
                self.imu.reset_yaw()
        # else means that the drive is overriden and in this case want to run autonomous tasks
        else:
            pass
            """#testing the turning to a certain angle
            if self.controller.getLeftTriggerAxis() == 1:
                self.drive.set_robot_to_angle(90)

            elif self.controller.getRightTriggerAxis() == 1:
                self.drive.set_robot_to_angle(270)

            elif self.controller.getXButton():
                self.drive.set_robot_to_angle(0)"""

            
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
#py -3 -m robotpy deploy