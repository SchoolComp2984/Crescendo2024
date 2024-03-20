from wpilib import Timer

from subsystems.drive import Drive
from subsystems.arm import Arm
from subsystems.shooter import Shooter
from subsystems.intake import Intake

#switches on robot that change values to run different autonomous codes for each.
class Autonomous:
    def __init__(self, _drive : Drive, _arm : Arm, _shooter : Shooter, _intake : Intake):
        # create instance of wpilib timer for auto timing
        self.timer = Timer()

        self.IDLE = 0
        self.REVVING_1 = 1
        self.SHOOTING_1 = 2
        self.BACKING_UP = 3
        self.TURNING = 4
        self.INTAKING = 5
        self.REVVING_2 = 6
        self.SHOOTING_2 = 7
        self.FINISHED = 8
        self.stage = self.IDLE
        
        self.drive = _drive
        self.arm = _arm
        self.shooter = _shooter
        self.intake = _intake

        self.revving_1_start_time = 0.0
        self.shooting_1_start_time = 0.0
        self.backing_up_start_time = 0.0
        self.intaking_start_time = 0.0
        self.revving_2_start_time = 0.0
        self.shooting_2_start_time = 0.0

        self.turning_start_angle = 0.0

    # shoots pre-loaded note and backs up out of community
    def one_note_auto(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.REVVING_1
            self.revving_1_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.REVVING_1:
            self.shooter.shooter_spin(1)
            
            if self.revving_1_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING_1
                self.shooting_1_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.SHOOTING_1:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            if self.shooting_1_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.BACKING_UP
                self.backing_up_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.BACKING_UP:
            self.drive.tank_drive(-0.5, -0.5)

            if self.backing_up_start_time + 3 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED

        if self.stage == self.FINISHED:
            pass

    # shoots pre-loaded note, backs up out of community, turns, intakes another note, and shoots it
    def two_note_auto(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.REVVING_1
            self.revving_1_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.REVVING_1:
            self.shooter.shooter_spin(1)

            # rev shooter motor for 1 second
            if self.revving_1_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING_1
                self.shooting_1_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.SHOOTING_1:
            # spin intake and shooter to feed note
            self.intake.intake_spin(1)
            self.shooter.shooter_spin(1)
        
            # feed for 1.5 seconds
            if self.shooting_1_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.BACKING_UP
                self.backing_up_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.BACKING_UP:
            # drive backward for 3 seconds at 0.5 speed
            self.drive.tank_drive(-0.5, -0.5)

            if self.backing_up_start_time + 3 < self.timer.getFPGATimestamp():
                self.stage = self.TURNING
                self.turning_start_angle = self.drive.drive_imu.get_yaw()

        elif self.stage == self.TURNING:
            # calculate how far we have turned relative to our angle before starting to turn
            turning_distance = abs(self.drive.drive_imu.get_yaw() - self.turning_start_angle)

            # if we are not within 3 degrees of 180 degrees of rotation, keep turning
            # else, move on to the next stage
            if not abs(turning_distance - 180) < 3:
                self.drive.tank_drive(-0.3, 0.3)
            else:
                self.stage = self.INTAKING

        
        elif self.stage == self.INTAKING:
            # drive forward for 2 seconds and spin intake
            self.drive.tank_drive(0.4, 0.4)
            self.intake.intake_spin(1)

            if self.intaking_start_time + 2 < self.timer.getFPGATimestamp():
                self.stage = self.REVVING_2
                self.revving_2_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.REVVING_2:
            # rev shooter motor for 1 second
            self.shooter.shooter_spin(1)

            if self.revving_2_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING_2
                self.shooting_2_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.SHOOTING_2:
            # spin intake and shooter for 1.5 seconds to feed note
            self.intake.intake_spin(1)
            self.shooter.shooter_spin(1)

            if self.shooting_2_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED
        
        elif self.stage == self.FINISHED:
            pass


