from wpilib import Timer

class AutoShoot:
    def __init__(self, _intake, _shooter):
        self.intake = _intake
        self.shooter = _shooter

        self.IDLE = 0
        self.REVVING = 1
        self.SHOOTING = 2
        self.auto_shoot_stage = self.IDLE

        self.timer = Timer()
        self.revving_start_time = 0.0
        self.shooting_start_time = 0.0


    def auto_shoot(self):
        # check if we are idling and ready to start auto shoot
        if self.auto_shoot_stage == self.IDLE:
            # stop spinning the intake and shooter motors
            self.intake.stop()
            self.shooter.stop()

            # set start time for intaking to current time
            self.revving_start_time = self.timer.getFPGATimestamp()

            # set stage to intaking
            self.auto_shoot_stage = self.REVVING

        # check if we are revving
        elif self.auto_shoot_stage == self.REVVING:
            # rev shooter motors
            self.shooter.shooter_spin(0.6)

            # check if we have been spinning shooter motors for 1.75 seconds
            if self.revving_start_time + 1.75 < self.timer.getFPGATimestamp():
                # set start time for shooint to current time
                self.shooting_start_time = self.timer.getFPGATimestamp()

                # set stage to shooting the note
                self.auto_shoot_stage = self.SHOOTING

        # check if we are shooting
        elif self.auto_shoot_stage == self.SHOOTING:
            # spin the shooter and intake motors
            self.shooter.shooter_spin(0.6)
            self.intake.intake_spin(1)

            # check if we have been shooting the note for 1 second
            # it should shoot within 2 seconds
            if self.shooting_start_time + 1 < self.timer.getFPGATimestamp():
                # we are done so set auto stage to idle
                self.auto_shoot_stage = self.IDLE


