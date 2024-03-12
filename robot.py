# import necessary libraries
# wpilib contains useful classes and methods for interfacing with parts of our robot such as sensors and even the driver station
import wpilib

# phoenix5 contains classes and methods to inferface with motors distributed by cross the road electronics
# third party library
import phoenix5

#importing rev libraries for our neo motors
import rev

#IMPORTING OUR COMMANDS
#import our Autonomous
from commands.autonomous import Autonomous

#import our shooting (manual)
from commands.auto_shoot import AutoShoot

# import our auto shooting tested on 3/6 meeting
from commands.auto_shoot_manual import AutoShootManual

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

        # create instance of our driver controller
        # it is a logitech x3d pro flight joystick
        self.driver_controller = wpilib.Joystick(constants.DRIVER_CONTROLLER_ID)

        # create an instance of our operator controller
        # it is an xbox controller at id constants.CONTROLLER_ID, which is 1
        self.operator_controller = wpilib.XboxController(constants.OPERATOR_CONTROLLER_ID)

        #create an instance of our amping function
        self.auto_amp = Auto_Amp(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)

        #create an instance for the auto shoot
        self.auto_shoot = AutoShoot(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)

        # create instance of auto shoot class
        self.auto_shoot_manual = AutoShootManual(self.intake, self.shooter)

        #instance for the auto intake
        self.auto_intake = Auto_Intake(self.arm, self.drive, self.intake, self.imu, self.networking)

        # override variables  to prevent spinning the same motors in multiple places in the code
        self.drive_override = False
        self.intake_override = False
        self.shoot_override = False
        self.arm_override = False


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
        if not self.arm_override:
            # X button -> arm inside chassis
            if self.operator_controller.getXButton():
                self.arm.shooting_override = False
                self.arm.desired_position = 60
            
            # Up arrow -> blocking arm position
            elif self.operator_controller.getPOV() == 0:
                self.arm.shooting_override = False
                self.arm.desired_position = 77

            # Down arrow -> source arm position
            # using for down position for now 3/11
            elif self.operator_controller.getPOV() == 180:
                self.arm.shooting_override = False
                self.arm.desired_position = 15

            self.arm.arm_to_angle(self.arm.desired_position)


        if not self.intake_override:
            # Y button -> forward intake
            if self.operator_controller.getYButton():
                self.intake.intake_spin(1)

            # Right Bumper -> reverse intake
            elif self.operator_controller.getRightBumper():
                self.intake.intake_spin(-1)

            # if neither pressed, stop intake
            else:
                self.intake.stop()

        if not self.shoot_override:
            # B button -> auto shoot
            if self.operator_controller.getBButton():
                self.auto_shoot_manual.auto_shoot()
                self.arm.shooting_override = True

            # Right Trigger -> manual shoot
            elif self.operator_controller.getRightTriggerAxis() == 1:
                self.auto_shoot.auto_shoot()

            # neither are pressed, stop shooter
            else:
                self.shooter.stop()
                
        #WORKING DRIVE CODE
        if not self.drive_override:
            # get the x and y axis of the left joystick on our controller
            joystick_x = self.driver_controller.getX()

            # rember that y joystick is inverted
            # multiply by -1;
            # "up" on the joystick is -1 and "down" is 1
            joystick_y = self.driver_controller.getY() * -1

            # get the twist of our driver joystick
            joystick_turning = self.driver_controller.getTwist()

            # run field oriented drive based on joystick values
            self.drive.field_oriented_drive(joystick_x, joystick_y, joystick_turning)
            
            # if we click button 11 on the flight stick, reset the IMU yaw
            if self.driver_controller.getRawButton(11):
                self.imu.reset_yaw()
        
# run our robot code
if __name__ == "__main__":
    wpilib.run(MyRobot)

# the command that deploys our code to our robot:
#py -3 -m robotpy deploy