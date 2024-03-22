from subsystems.drive import Drive
from subsystems.intake import Intake
from subsystems.networking import NetworkReciever

from commands.descend import Descend

from wpilib import Timer


class AutoIntake:
    def __init__(self, _drive : Drive, _descend : Descend, _intake : Intake, _networking : NetworkReciever):
        # stages that make up auto inake
        self.IDLE = 0
        self.ARM_DOWN = 1
        self.ALIGNING = 2
        self.DRIVE_AND_INTAKE = 3
        self.FINISHED = 4
        self.stage = self.IDLE

        self.drive = _drive
        self.descend = _descend
        self.intake = _intake
        self.networking = _networking

        self.timer = Timer()
        self.drive_and_intake_start_time = 0.0

    def auto_intake(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage == self.ARM_DOWN

        elif self.stage == self.ARM_DOWN:
            self.descend.auto_descend()

            if self.descend.stage == self.descend.FINISHED:
                self.descend.stage = self.descend.IDLE

                self.stage = self.ALIGNING


        elif self.stage == self.ALIGNING:
            # x position of note that we need to check if the note is aligned (in the middle of the camera POV)
            note_x = self.networking.get_note_data()[0]

            # return if we don't see a note
            if note_x is None:
                return
            
            # if we are to the left, rotate left
            if note_x < -5:
                self.drive.tank_drive(-0.1, 0.1)

            # if we are to the right, rotate right
            elif note_x > 5:
                self.drive.tank_drive(0.1, -0.1)

            # if the note is aligned, move on to driving and intaking
            else:
                self.stage = self.DRIVE_AND_INTAKE
                self.drive_and_intake_start_time = self.timer.getFPGATimestamp()

        elif self.stage == self.DRIVE_AND_INTAKE:
            # drive forward and spin intake motors
            self.drive.tank_drive(0.3, 0.3)
            self.intake.intake_spin(1)

            if self.drive_and_intake_start_time + 3 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.stage = self.IDLE

        

