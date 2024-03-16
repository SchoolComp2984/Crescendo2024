from wpilib import Timer

from subsystems.arm import Arm
from subsystems.shooter import Shooter
from subsystems.intake import Intake

class ManualShoot:
    def __init__(self, _arm, _shooter, _intake):
        self.arm = _arm
        self.shooter = _shooter
        self.intake = _intake

        self.IDLE = 0
        self.RAISING_ARM = 1
        self.REVVING = 2
        self.SHOOTING = 3
        self.FINISHED = 4
        self.stage = self.IDLE

        self.timer = Timer()
        self.revving_start_time = 0.0
        self.shooting_start_time = 0.0

        self.running = False

    def manual_shoot(self, angle):
        if not self.running:
            return

        # check if we are idling and ready to start auto shoot
        if self.stage == self.IDLE:
            # stop spinning the intake and shooter motors
            self.intake.stop()
            self.shooter.stop()

            self.stage = self.stage = self.RAISING_ARM

        elif self.stage == self.RAISING_ARM:
            self.arm.desired_position = angle

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 3:
                self.revving_start_time = self.timer.getFPGATimestamp()

                self.stage = self.REVVING

        # check if we are revving
        elif self.stage == self.REVVING:
            # rev shooter motors
            self.shooter.shooter_spin(1)
            
            # enable arm shooting override
            self.arm.shooting_override = True

            # check if we have been spinning shooter motors for 1.75 seconds
            if self.revving_start_time + 1.75 < self.timer.getFPGATimestamp():
                # set start time for shooint to current time
                self.shooting_start_time = self.timer.getFPGATimestamp()

                # set stage to shooting the note
                self.stage = self.SHOOTING

        # check if we are shooting
        elif self.stage == self.SHOOTING:
            # spin the shooter and intake motors
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            # check if we have been shooting the note for 1 second
            # it should shoot within 2 seconds
            if self.shooting_start_time + 1 < self.timer.getFPGATimestamp():
                # we are done so set auto stage to finished
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            # checks before going back blah blah
            self.running = False


