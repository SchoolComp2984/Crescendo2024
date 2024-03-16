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
from commands.interpolated_shoot import InterpolatedShoot
from commands.manual_shoot import ManualShoot
from commands.auto_amp import AutoAmp
from commands.auto_intake import AutoIntake
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
        self.manual_shoot = ManualShoot(self.intake, self.shooter, self.arm)
        self.auto_shoot = InterpolatedShoot(self.manual_shoot, self.drive, self.networking)
        self.auto_amp = AutoAmp(self.arm, self.drive, self.shooter, self.intake, self.imu, self.networking)
        self.auto_intake = AutoIntake(self.arm, self.drive, self.intake, self.imu, self.networking)
        self.descend = Descend(self.arm)


        """# override variables to enable/disable certain functionalities of our robot
        self.drive_override = False
        self.intake_override = False
        self.shoot_override = False
        self.arm_override = False"""

        self.override = False

        # switch to turn on or off drive
        self.enable_drive = True

        self.climbing = False

    # setup before our robot transitions to autonomous
    def autonomousInit(self):
        # print if our IMU is ready to be used
        if self.arm_imu.is_ready(): print("arm_imu is in fact ready")

        # create instance of our autonomous code
        self.autonomous = Autonomous(self.drive, self.arm, self.shooter, self.intake)



    # ran every 20 ms during autonomous mode
    def autonomousPeriodic(self):
        pass


    # setup before our robot transitions to teleop (where we control with a joystick or custom controller)
    def teleopInit(self):
        # print if our IMU is ready to be used
        if self.arm_imu.is_ready(): print("arm_imu is in fact ready")

        self.climbing = False
        


    # ran every 20 ms during teleop
    def teleopPeriodic(self):
        # print arm data
        print(f"des.: {self.arm.desired_position}, angle: {self.arm.get_arm_pitch()}, gravity: {self.arm.gravity_compensation}")
        
        # RT -> manual shoot
        if self.operator_controller.getRightTriggerAxis() == 1:
            if self.manual_shoot.running == False:
                self.manual_shoot.running = True
                self.manual_shoot.stage = self.manual_shoot.IDLE

            if not self.manual_shoot.stage == self.manual_shoot.FINISHED:
                self.override = True
            else:
                self.override = False
        
        # Y button -> auto shoot speaker
        elif self.operator_controller.getYButton():
            if self.auto_shoot.running == False:
                self.auto_shoot.running = True
                self.auto_shoot.stage = self.auto_shoot.IDLE

            if not self.auto_shoot.stage == self.auto_shoot.FINISHED:
                self.override = True
            else:
                self.override = False

        # stop shooter if no shooter buttons are being pressed
        # none currently pressed -> no override
        else:
            self.shooter.stop()
            self.override = False
            

        # B button -> auto amp
        if self.operator_controller.getBButton():
            if self.auto_amp.running == False:
                self.auto_amp.running = True
                self.auto_amp.stage = self.auto_amp.IDLE

            if not self.auto_amp.stage == self.auto_amp.FINISHED:
                self.override = True
            else:
                self.override = False

        # Down arrow -> arm to intake position (descend)
        elif self.operator_controller.getPOV() == 180:
            if self.descend.running == False:
                self.descend.running = True
                self.descend.stage = self.descend.IDLE

            if not self.descend.stage == self.descend.FINISHED:
                self.override = True
            else:
                self.override = False

        # if none are pressed currenlty, do not override anything
        else:
            self.override = False


        if self.manual_shoot.running == True:
            self.manual_shoot.manual_shoot(20)

        elif self.auto_shoot.running == True:
            self.auto_shoot.auto_shoot()

        elif self.auto_amp.running == True:
            self.auto_amp.auto_amp()

        elif self.descend.running == True:
            self.descend.auto_descend()

        # if we are not holding an auto button down, essentially
        if not self.override:
            # ---------------- ARM ---------------- 
            # UP -> blocking position / amp position
            if self.operator_controller.getPOV() == 0:
                self.arm.shooting_override = False
                self.arm.desired_position = 80

            # RIGHT -> speaker/hover position
            if self.operator_controller.getPOV() == 90:
                self.arm.shooting_override = False
                self.arm.desired_position = 15

            # LEFT -> source arm position / inside chassis position
            elif self.operator_controller.getPOV() == 270:
                self.arm.shooting_override = False
                self.arm.desired_position = 70

            # Flight Stick Trigger -> down position:
            elif self.driver_controller.getTriggerPressed():
                self.arm.shooting_override = False
                self.arm.desired_position = 15

            # A button -> Climb (move arm all the way down)
            elif self.operator_controller.getAButtonPressed():
                self.climbing = True
                self.arm.set_speed(-1)
            
            if not self.climbing:
                self.arm.arm_to_angle(self.arm.desired_position)


            # ---------------- INTAKE ---------------- 

            if self.operator_controller.getXButton():
                self.shooter.shooter_spin(0.4)

            # RB -> forward intake
            if self.operator_controller.getRightBumper():
                self.intake.intake_spin(1)

            # LB -> reverse intake
            elif self.operator_controller.getLeftBumper():
                self.intake.intake_spin(-1)

            # if neither pressed, stop intake
            else:
                self.intake.stop()

            # ---------------- DRIVE ---------------- 
                
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
                if self.driver_controller.getRawButton(11):
                    self.imu.reset_yaw()
        
# run our robot code
if __name__ == "__main__":
    wpilib.run(MyRobot)

# the command that deploys our code to our robot:
#py -3 -m robotpy deploy
