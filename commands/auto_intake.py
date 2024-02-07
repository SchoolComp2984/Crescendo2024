#imported intake class to drive intake motors
from subsystems.intake import Intake

class Auto_Intake:
    def _init__(self, _arm, _drive, _intake, _imu):
        #stages for autonomously intaking
        self.INTAKE_IDLE = 0 #idle, not doing anything
        self.FIND_NOTE_POS = 1 #find the note position
        self.ROTATE_ROBOT = 2 #rotate the robot to be in line with the note
        self.MOVE_ARM = 3 #move the arm to intake position
        self.SPIN_INTAKE = 4 #start spinning the intake motors
        self.DRIVE_TO_NOTE = 5 #drive towards the note and pickup note
        self.RESET_ARM = 6 #reset the arm to default position and stop the intake motors
        self.INTAKE_DONE = 7 #done with intaking
        self.intake_stage = self.INTAKE_IDLE

    def scan_for_note(self):
        """
        scan for the note
        return true when done

        """
        pass
        
    def rotate_robot(self):
        """
        rotate the robot to be in line with the note
        return true when done
        
        """
        pass

    def move_arm(self):
        """
        Move the arm to the intake position.
        return true when done

        """
        pass

    def spin_intake_motors(self):
        """
        spin the intake motors. 
        DO NOT STOP spinning them; will stop in DRIVE_TO_NOTE
        return true when done

        """
        pass

    def drive_to_note(self):
        """
        Drive to the note.
        Stop spinning the intake motors after the note is intaked.
        return true when done

        """
        pass

    def reset_arm_position(self):
        """
        Reset the arm to default position
        return true when done

        """
        pass

    def autonomous_intake(self):
        if self.intake_stage == self.INTAKE_IDLE:
            self.intake_stage == self.FIND_NOTE_POS

        elif self.intake_stage == self.FIND_NOTE_POS:
            if self.scan_for_note():
                self.intake_stage == self.ROTATE_ROBOT

        elif self.intake_stage == self.ROTATE_ROBOT:
            if self.rotate_robot():
                self.intake_stage == self.MOVE_ARM

        elif self.intake_stage == self.MOVE_ARM:
            if self.move_arm():
                self.intake_stage == self.SPIN_INTAKE

        elif self.intake_stage == self.SPIN_INTAKE:
            if self.spin_intake_motors():
                self.intake_stage == self.DRIVE_TO_NOTE

        elif self.intake_stage == self.DRIVE_TO_NOTE:
            if self.drive_to_note():
                self.intake_stage == self.RESET_ARM

        elif self.intake_stage == self.RESET_ARM:
            if self.reset_arm_position():
                self.intake_stage == self.INTAKE_DONE

        elif self.intake_stage == self.INTAKE_DONE:
            self.intake_stage = self.INTAKE_IDLE

        

