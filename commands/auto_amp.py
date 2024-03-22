# import timer class we need from wpilib
from wpilib import Timer

from subsystems.drive import Drive
from subsystems.arm import Arm
from subsystems.shooter import Shooter
from subsystems.intake import Intake
from subsystems.networking import NetworkReciever

class AutoAmp:
    def __init__(self, _drive : Drive, _arm : Arm, _shooter : Shooter, _intake : Intake, _networking : NetworkReciever):
        # stages for using the amp.
        #iterating through these stages with a tracker that will move on to the next stage after the current one is finished.
        self.IDLE = 0
        self.ALIGN = 1
        self.DRIVING = 2
        self.MOVE_ARM = 3
        self.MOTOR_SPIN = 4
        self.RETURN_ARM = 5
        self.FINISHED = 6
        self.stage = self.IDLE

        self.drive = _drive
        self.arm = _arm
        self.shooter = _shooter
        self.intake = _intake
        self.networking = _networking

        # create instance of timer
        self.timer = Timer()

        # init start time variables
        self.motor_spin_start_time = 0.0

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
                self.stage = self.DRIVING

        elif self.stage == self.DRIVING:
            apriltag_distance = self.networking.get_apriltag_data()[2]

            if apriltag_distance is None:
                return

            if apriltag_distance > 0.2:
                self.drive.tank_drive(0.2, 0.2)

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
            self.stage = self.IDLE