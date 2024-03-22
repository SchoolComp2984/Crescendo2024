from utils.math_functions import interpolation_array

from subsystems.drive import Drive
from subsystems.arm import Arm
from subsystems.shooter import Shooter
from subsystems.intake import Intake
from subsystems.networking import NetworkReciever

from wpilib import Timer

class AutoShoot:
    def __init__(self, _drive : Drive, _arm : Arm, _shooter : Shooter, _intake : Intake, _networking : NetworkReciever):
        self.IDLE = 0
        self.ALIGNING = 1
        self.MOVING_ARM = 2
        self.DELAY = 3
        self.INTAKING = 4
        self.REVVING = 5
        self.SHOOTING = 6
        self.FINISHED = 7
        self.stage = self.IDLE

        self.timer = Timer()
        self.intaking_start_time = 0.0
        self.revving_start_time = 0.0
        self.shooting_start_time = 0.0
        self.delay_start_time = 0.0

        self.drive = _drive
        self.arm = _arm
        self.shooter = _shooter
        self.intake = _intake
        self.networking = _networking

        self.distance = -1

    def angle_interpolation(self, value):
        arr = [ \
        [0, 25],\
        [5, 40]]

        return interpolation_array(value, arr)

    def basic_shoot(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.MOVING_ARM

        elif self.stage == self.MOVING_ARM:
            self.arm.desired_position = 27

            if abs(22.5 - self.arm.get_arm_pitch()) < 5:
                self.stage = self.INTAKING
                self.intaking_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.INTAKING:
            self.intake.intake_spin(1)

            if self.intaking_start_time + 0.5 < self.timer.getFPGATimestamp() and abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 4:
                self.stage = self.REVVING
                self.revving_start_time = self.timer.getFPGATimestamp()
                self.arm.shooting_override = True

        elif self.stage == self.REVVING:
            self.shooter.shooter_spin(1)

            if self.revving_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING
                self.shooting_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.SHOOTING:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            if self.shooting_start_time + 2 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            pass

    def interpolated_shoot(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.ALIGNING
            print("aligning")

        elif self.stage == self.ALIGNING:
            apriltag_data = self.networking.get_apriltag_data()

            sees_tag = apriltag_data[4]

            if not sees_tag:
                return

            apriltag_x = apriltag_data[0]
            self.distance = apriltag_data[2]

            if abs(apriltag_x) < 10:
                self.stage = self.MOVING_ARM
                print("moving arm")


            # rotate left if apriltag is to the left
            if apriltag_x < 0:
                self.drive.mecanum_drive_robot_oriented(0, 0, -0.3)
            elif apriltag_x > 0:
                self.drive.mecanum_drive_robot_oriented(0, 0, 0.3)

        elif self.stage == self.MOVING_ARM:
            angle = self.angle_interpolation(self.distance)

            self.arm.desired_position = angle

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 5:
                self.stage = self.DELAY
                self.delay_start_time = self.timer.getFPGATimestamp()
                print("delaying")

        elif self.stage == self.DELAY:
            if self.delay_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.REVVING
                self.arm.shooting_override = True
                self.revving_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.REVVING:
            self.shooter.shooter_spin(1)

            if self.revving_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING
                self.shooting_start_time = self.timer.getFPGATimestamp()
                print("shooting")

        elif self.stage == self.SHOOTING:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            if self.shooting_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED
                print("done")

        elif self.stage == self.FINISHED:
            pass

            