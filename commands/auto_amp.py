# import timer class we need from wpilib
from wpilib import Timer

class AutoAmp:
    def __init__(self, _arm, _drive, _shooter, _intake, _imu, _networking):
        # stages for using the amp.
        #iterating through these stages with a tracker that will move on to the next stage after the current one is finished.
        self.IDLE = 0
        self.ALIGN = 1
        self.MOVE_ARM = 2
        self.MOTOR_SPIN = 3
        self.RETURN_ARM = 4
        self.FINISHED = 5
        self.stage = self.IDLE

        #reference to the arm
        self.arm = _arm

        #reference to the drive
        self.drive = _drive

        #reference to the shooter
        self.shooter = _shooter
        
        #reference to the intake
        self.intake = _intake

        #referencing imu
        self.imu = _imu

        #referencing networking
        self.networking = _networking

        # create instance of timer
        self.timer = Timer()

        # init start time variables
        self.motor_spin_start_time = 0.0

        self.running = False

    def auto_amp(self):
        #status tracker that goes through all the different steps of amping
        if self.stage == self.IDLE:
            self.stage = self.ALIGN

        elif self.stage == self.ALIGN:
            apriltag_x = self.networking.get_apriltag_data()[0]

            if apriltag_x is None:
                return

            if apriltag_x < -8:
                self.drive.mecanum_drive_robot_oriented(-0.3, 0, 0)

            elif apriltag_x > 8:
                self.drive.mecanum_drive_robot_oriented(0.3, 0, 0)

            else:
                self.stage = self.MOVE_ARM

        elif self.stage == self.MOVE_ARM:
            self.arm.desired_position = 80

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 4:
                self.stage = self.MOTOR_SPIN
                self.motor_spin_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.MOTOR_SPIN:
            self.intake.intake_spin(1)
            self.shooter.shooter_spin(0.4)

            if self.motor_spin_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.RETURN_ARM

        elif self.stage == self.RETURN_ARM:
            self.arm.desired_position = 60

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 4:
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.running = False
