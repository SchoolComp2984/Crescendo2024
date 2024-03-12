
class AutoIntake:
    def __init__(self, _arm, _drive, _intake, _imu, _networking):
        #stages for autonomously intaking
        self.INTAKE_IDLE = 0 #idle, not doing anything
        self.FIND_NOTE = 1 #find the note position, turn so that we're facing the note.
        self.MOVE_ARM = 2 #move the arm to intake position
        self.INTAKE_NOTE = 3 #start spinning the intake motors
        self.RESET_ARM = 4 #reset the arm to default position and stop the intake motors
        self.INTAKE_DONE = 5 #done with intaking
        self.intake_stage = self.INTAKE_IDLE

        #reference the arm
        self.arm = _arm

        #reference the drive
        self.drive = _drive

        #refence the intake
        self.intake = _intake

        #reference the imu
        self.imu = _imu

        #reference the networking for scanning the apriltag and the note
        self.networking = _networking

        #intermediate variable that stores the note data so it can be accessed from anywhere
        self.note_data = None

    #scans for the note, sees if we see a note.
    def find_note(self):
        #array of note data.
        self.note_data = self.networking.get_note_data()

        #if the array length is not zero (so it actually exists and we get data back)
        if len(self.note_data) is not None:
            self.note_x = self.note_data[0]
            if abs(self.note_x) < 20: return True
            elif self.note_x < -20:
                self.drive.tank_drive(-.5 , .5)
            elif self.note_x > 20:
                self.drive.tank_drive(.5, -.5)
    
    def move_arm(self):
        """
        Move the arm to the intake position.
        return true when done
        """
        pass

    #after the arm is in the right position
    def intake_note(self):
        self.intake.intake_spin(1)
        self.drive.tank_drive(.3, .3)
        self.note_distance  = self.note_data[2]
        if self.note_distance < .05:
            return True

    def reset_arm_position(self):
        """
        Reset the arm to default position
        return true when done
        """
        pass

    def autonomous_intake(self):
        if self.intake_stage == self.INTAKE_IDLE:
            self.intake_stage == self.FIND_NOTE

        elif self.intake_stage == self.FIND_NOTE:
            if self.find_note():
                self.intake_stage == self.MOVE_ARM

        elif self.intake_stage == self.MOVE_ARM:
            if self.move_arm():
                self.intake_stage == self.INTAKE_NOTE

        elif self.intake_stage == self.INTAKE_NOTE:
            if self.intake_note():
                self.intake_stage == self.RESET_ARM

        elif self.intake_stage == self.RESET_ARM:
            if self.reset_arm_position():
                self.intake_stage == self.INTAKE_DONE

        elif self.intake_stage == self.INTAKE_DONE:
            self.intake_stage = self.INTAKE_IDLE

        

