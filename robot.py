# import necessary libraries for interfacing with joysticks, driverstations, and hardware from different manufacturers
import wpilib
import phoenix5
import rev

# import subsystems
from subsystems.drive import Drive
from subsystems.shooter import Shooter
from subsystems.networking import NetworkReciever
from subsystems.intake import Intake
from subsystems.arm import Arm
from subsystems.imu import IMU

# import commands
from commands.auto_shoot import AutoShoot
from commands.manual_shoot import ManualShoot
from commands.auto_amp import AutoAmp
from commands.auto_intake import AutoIntake
from commands.climb import Climb
from commands.descend import Descend

# import autonomous code
from commands.autonomous import Autonomous

# import our constants which serve as "settings" for our robot/code, mainly IDs for CAN devices - motors, IMUs, and controllers
from utils import constants

# create our base robot class
class MyRobot(wpilib.TimedRobot):
    # initialize motors and sensors - create references to physical parts of our robot
    def robotInit(self):
        # create reference to our Falcon 500 motors for driving
        self.front_right = phoenix5._ctre.WPI_TalonFX(constants.FRONT_RIGHT_ID)
        self.front_left = phoenix5._ctre.WPI_TalonFX(constants.FRONT_LEFT_ID)
        self.back_left = phoenix5._ctre.WPI_TalonFX(constants.BACK_LEFT_ID)
        self.back_right = phoenix5._ctre.WPI_TalonFX(constants.BACK_RIGHT_ID)

        # invert the motors on the right side of our robot
        self.front_right.setInverted(True)
        self.back_right.setInverted(True)


        # create a reference to our IMU
        self.imu_motor_controller = phoenix5._ctre.WPI_TalonSRX(constants.IMU_ID)
        self.imu = IMU(self.imu_motor_controller)


        #create reference to our Falcon motors
        self.shooter_upper_motor = phoenix5._ctre.WPI_TalonFX(constants.SHOOTER_UPPER_MOTOR_ID)
        self.shooter_lower_motor = phoenix5._ctre.WPI_TalonFX(constants.SHOOTER_LOWER_MOTOR_ID)

        self.shooter_upper_motor.setInverted(True)
        self.shooter_lower_motor.setInverted(True)


        # create reference to our intake motor
        self.intake_motor = rev.CANSparkMax(constants.INTAKE_MOTOR_ID, rev.CANSparkLowLevel.MotorType.kBrushless)


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


        # instances of our subsystems - passing in references to motors, sensors, etc.
        self.arm = Arm(self.arm_motor_left_front, self.arm_motor_left_back, self.arm_motor_right_front, self.arm_motor_right_back, self.arm_imu)
        self.intake = Intake(self.intake_motor)
        self.drive = Drive(self.front_right, self.front_left, self.back_left, self.back_right, self.imu)
        self.shooter = Shooter(self.shooter_lower_motor, self.shooter_upper_motor)
        
        
        # instance of networking class to recieve information from raspberry pis
        self.networking = NetworkReciever()

        # create instance of our driver controller (flight stick) and operator controller (xbox controller)
        self.driver_controller = wpilib.Joystick(constants.DRIVER_CONTROLLER_ID)
        self.operator_controller = wpilib.XboxController(constants.OPERATOR_CONTROLLER_ID)

        #create instances of autonomous abilities for our robot
        self.auto_shoot = AutoShoot(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)
        self.manual_shoot = ManualShoot(self.intake, self.shooter, self.arm)
        self.auto_amp = AutoAmp(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)
        self.auto_intake = AutoIntake(self.arm, self.drive, self.intake, self.imu, self.networking)
        self.climb = Climb(self.arm)
        self.descend = Descend(self.arm)


        # override variables to enable/disable certain functionalities of our robot
        self.drive_override = False
        self.intake_override = False
        self.shoot_override = False
        self.arm_override = False



    # setup before our robot transitions to autonomous
    def autonomousInit(self):
        # print if our IMU is ready to be used
        if self.arm_imu.is_ready(): print("arm_imu is in fact ready")

        # create instance of our autonomous code
        self.autonomous = Autonomous()



    # ran every 20 ms during autonomous mode
    def autonomousPeriodic(self):
        pass



    # setup before our robot transitions to teleop (where we control with a joystick or custom controller)
    def teleopInit(self):
        # print if our IMU is ready to be used
        if self.arm_imu.is_ready(): print("arm_imu is in fact ready")
        


    # ran every 20 ms during teleop
    def teleopPeriodic(self):
        # print arm data
        print(f"des.: {self.arm.desired_position}, angle: {self.arm.get_arm_pitch()}, gravity: {self.arm.gravity_compensation}")

        if not self.arm_override:
            # UP -> blocking position
            if self.operator_controller.getPOV() == 0:
                self.arm.shooting_override = False
                self.arm.desired_position = 80

            # RIGHT -> inside chassis
            if self.operator_controller.getPOV() == 90:
                self.arm.shooting_override = False
                self.arm.desired_position = 65

            # DOWN -> ground intake position
            elif self.operator_controller.getPOV() == 180:
                self.descend.descending = True

            # LEFT -> source arm position
            elif self.operator_controller.getPOV() == 270:
                self.arm.shooting_override = False
                self.arm.desired_position = 70

            # Flight Stick Trigger -> down position:
            elif self.driver_controller.getTriggerPressed():
                self.arm.shooting_override = False
                self.arm.desired_position = 15

            # check if we should be descending then run descend code
            if self.descend.descending:
                self.arm.shooting_override = False
                self.descend.auto_descend()

            # set arm to desired angle
            self.arm.arm_to_angle(self.arm.desired_position)

        if not self.intake_override:
            # RB -> forward intake
            if self.operator_controller.getRightBumper():
                self.intake.intake_spin(1)

            # LB -> reverse intake
            elif self.operator_controller.getLeftBumper():
                self.intake.intake_spin(-1)

            # if neither pressed, stop intake
            else:
                self.intake.stop()

        if not self.shoot_override:
            # RT -> manual shoot
            if self.operator_controller.getRightTriggerAxis() == 1:
                self.manual_shoot.shooting = True

            # Y -> auto shoot
            elif self.operator_controller.getYButton() == 1:
                self.auto_shoot.auto_shoot()

            # neither are pressed, stop shooter
            else:
                self.shooter.stop()

            if self.manual_shoot.shooting == True:
                self.manual_shoot.manual_shoot()

        if not self.drive_override:
            # get the x and y axis of the left joystick on our controller
            joystick_x = self.driver_controller.getX()

            # rember that y joystick is inverted
            # multiply by -1;
            # "up" on the joystick is -1 and "down" is 1
            joystick_y = self.driver_controller.getY() * -1

            # get the twist of our driver joystick
            joystick_turning = self.driver_controller.getZ()

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
