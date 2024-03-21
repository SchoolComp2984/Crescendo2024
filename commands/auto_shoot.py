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
        self.REVVING = 4
        self.SHOOTING = 5
        self.FINISHED = 6
        self.stage = self.IDLE

        self.timer = Timer()
        self.delay_start_time = 0.0
        self.revving_start_time = 0.0
        self.shooting_start_time = 0.0

        self.drive = _drive
        self.arm = _arm
        self.shooter = _shooter
        self.intake= _intake
        self.networking = _networking

        self.distance = -1

    def angle_interpolation(self, value):
        arr = [ \
        [0, 0],\
        [8, 35]]

        return interpolation_array(value, arr)

    def basic_shoot(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.MOVING_ARM
            print("starting auto shoot")

        elif self.stage == self.MOVING_ARM:
            self.arm.desired_position = 15

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 5:
                self.stage = self.DELAY
                self.delay_start_time = self.timer.getFPGATimestamp()
                print("done moving arm")

        elif self.stage == self.DELAY:
            if self.delay_start_time + 1 < self.timer.getFPGATimestamp() and abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 4:
                print("done delay")
                self.stage = self.REVVING
                self.revving_start_time = self.timer.getFPGATimestamp()
                self.arm.shooting_override = True


        elif self.stage == self.REVVING:
            self.shooter.shooter_spin(1)

            if self.revving_start_time + 1.5 < self.timer.getFPGATimestamp():
                print("done revving starting shoot")
                self.stage = self.SHOOTING
                self.shooting_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.SHOOTING:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            if self.shooting_start_time + 1 < self.timer.getFPGATimestamp():
                print("done shooting")
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            print("done auto shoot")
            pass

    def interpolated_shoot(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.ALIGNING

        elif self.stage == self.ALIGNING:
            apriltag_data = self.networking.get_apriltag_data()

            apriltag_x = apriltag_data[0]

            self.distance = apriltag_data[2]

            # don't shoot if we cannot see april tag OR april tag we are seeing is not for the speaker
            # add check to see that it is the correct one
            if apriltag_x is None:
                return
            
            # rotate left if apriltag is to the left
            if apriltag_x < -5:
                self.drive.tank_drive(-0.1, 0.1)
            elif apriltag_x > 5:
                self.drive.tank_drive(0.1, -0.1)
            else:
                self.stage = self.MOVING_ARM

        if self.stage == self.MOVING_ARM:
            angle = self.angle_interpolation(self.distance)

            self.arm.desired_position = angle

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 4:
                self.stage = self.REVVING
                self.revving_start_time = self.timer.getFPGATimestamp()
                self.arm.shooting_override = True


        elif self.stage == self.REVVING:
            self.shooter.shooter_spin(1)

            if self.revving_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING
                self.shooting_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.SHOOTING:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            if self.shooting_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            pass

            