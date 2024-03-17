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
from subsystems.color_sensor import ColorSensor

# import commands
from commands.interpolated_shoot import InterpolatedShoot
from commands.auto_amp import AutoAmp
from commands.auto_intake import AutoIntake
from commands.descend import Descend
from commands.climb import Climb

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

        # reference to climb motor
        self.cimb_motor = rev.CANSparkMax(constants.CLIMB_MOTOR_ID, rev.CANSparkLowLevel.MotorType.kBrushless)

        # reference to the color sensor inside our intake
        self.color_sensor_reference = rev.ColorSensorV3(wpilib.I2C.Port(0))

        # instances of our subsystems - passing in references to motors, sensors, etc.
        self.arm = Arm(self.arm_motor_left_front, self.arm_motor_left_back, self.arm_motor_right_front, self.arm_motor_right_back, self.arm_imu)
        self.intake = Intake(self.intake_motor)
        self.drive = Drive(self.front_right, self.front_left, self.back_left, self.back_right, self.imu)
        self.shooter = Shooter(self.shooter_lower_motor, self.shooter_upper_motor)
        self.color_sensor = ColorSensor(self.color_sensor_reference)

        # instance of networking class to recieve information from raspberry pis
        self.networking = NetworkReciever()

        # create instance of our driver controller (flight stick) and operator controller (xbox controller)
        self.driver_controller = wpilib.Joystick(constants.DRIVER_CONTROLLER_ID)
        self.operator_controller = wpilib.XboxController(constants.OPERATOR_CONTROLLER_ID)

        #create instances of autonomous abilities for our robot
        self.auto_shoot = InterpolatedShoot(self.drive, self.arm, self.shooter, self.intake, self.networking)
        self.auto_amp = AutoAmp(self.drive, self.arm, self.shooter, self.intake, self.networking)
        self.descend = Descend(self.arm)
        self.auto_intake = AutoIntake(self.drive, self.descend, self.intake, self.networking, self.color_sensor)
        self.climb = Climb(self.climb_motor)

        # switch to turn on or off drive
        self.enable_drive = True

    # setup before our robot transitions to autonomous
    def autonomousInit(self):
        # create instance of our autonomous code
        self.autonomous = Autonomous(self.drive, self.arm, self.shooter, self.intake)



    # ran every 20 ms during autonomous mode
    def autonomousPeriodic(self):
        pass


    # setup before our robot transitions to teleop (where we control with a joystick or custom controller)
    def teleopInit(self):
        self.climbing = False
    

    # ran every 20 ms during teleop
    def teleopPeriodic(self):
        # print(f"desired position: {self.arm.desired_position}, current position: {self.arm.get_arm_pitch()}")

        # get control buttons
        climb_button_pressed = self.operator_controller.getAButton()
        auto_amp_button_pressed = self.operator_controller.getBButton()
        auto_intake_button_pressed = self.operator_controller.getXButton()
        shoot_button_pressed = self.operator_controller.getYButton()
        amp_shoot_button_pressed = self.operator_controller.getRightTriggerAxis() == 1
        intake_button_pressed = self.operator_controller.getRightBumper()
        outtake_button_pressed = self.operator_controller.getLeftBumper() 
        amp_blocking_position_button_pressed = self.operator_controller.getPOV() == 0
        inside_chassis_position_button_pressed = self.operator_controller.getPOV() == 90
        intake_position_button_pressed = self.operator_controller.getPOV() == 180
        hover_position_button_pressed = self.operator_controller.getPOV() == 270
        under_stage_button_pressed = self.driver_controller.getTrigger()
        reset_imu_button_pressed = self.driver_controller.getRawButton(11)
       

        # ---------- INTAKE ----------
        if intake_button_pressed:
            self.intake.intake_spin(1)

        elif outtake_button_pressed:
            self.intake.intake_spin(-1)

        else:
            self.intake.stop()


        # auto functions
        if auto_amp_button_pressed:
            self.auto_amp.auto_amp()

        else:
            self.auto_amp.stage = self.auto_amp.IDLE


            if auto_intake_button_pressed:
                self.auto_intake.auto_intake()

            else:
                self.auto_intake.stage = self.auto_intake.IDLE

                if intake_position_button_pressed:
                    self.descend.descending = True



        if self.descend.descending:
            self.descend.auto_descend()



        # ---------- SHOOTER ----------
        if shoot_button_pressed:
            self.auto_shoot.interpolated_shoot()

            if self.auto_shoot.stage == self.auto_shoot.FINISHED:
                self.auto_shoot.stage = self.auto_shoot.IDLE

        else:
            self.auto_shoot.stage = self.auto_shoot.IDLE

            if amp_shoot_button_pressed:
                self.shooter.shooter_spin(0.4)

            else:
                self.shooter.stop()
        

        # ---------- ARM CONTROLS ----------
        if amp_blocking_position_button_pressed:
            self.arm.desired_position = 80

        elif inside_chassis_position_button_pressed:
            self.arm.desired_position = 60

        elif hover_position_button_pressed or under_stage_button_pressed:
            self.arm.desired_position = 15

        # set arm to position
        self.arm.arm_to_angle(self.arm.desired_position)


        # check if drive is enabled
        if self.enable_drive:
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
            if reset_imu_button_pressed:
                self.imu.reset_yaw()
        
# run our robot code
if __name__ == "__main__":
    wpilib.run(MyRobot)

# the command that deploys our code to our robot:
#py -3 -m robotpy deploy
