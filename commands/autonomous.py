from wpilib import Timer

from subsystems.drive import Drive
from subsystems.arm import Arm
from subsystems.shooter import Shooter
from subsystems.intake import Intake

from phoenix5.sensors import AbsoluteSensorRange
import phoenix5

#switches on robot that change values to run different autonomous codes for each.
class Autonomous:
    def __init__(self, _drive : Drive, _arm : Arm, _shooter : Shooter, _intake : Intake):
        # create instance of wpilib timer for auto timing
        self.timer = Timer()

        self.IDLE = 0
        self.KICKSTAND = 1
        self.DRIVING_FORWARD = 2
        self.MOVING_ARM_1 = 3
        self.REVVING_1 = 4
        self.SHOOTING_1 = 5
        self.DROPPING_ARM = 6
        self.BACKING_UP = 7
        self.MOVING_ARM_2 = 8
        self.REVVING_2 = 9
        self.SHOOTING_2 = 10
        self.BACKING_UP_FINAL = 11
        self.FINISHED = 12
        self.DELAY = 13
        self.DELAY_2 = 14
        self.stage = self.IDLE
        
        self.drive = _drive
        self.arm = _arm
        self.shooter = _shooter
        self.intake = _intake

        self.driving_forward_start_time = 0.0
        self.revving_1_start_time = 0.0
        self.shooting_1_start_time = 0.0
        self.dropping_arm_start_time = 0.0
        self.backing_up_start_time = 0.0
        self.intaking_start_time = 0.0
        self.revving_2_start_time = 0.0
        self.shooting_2_start_time = 0.0
        self.moving_arm_2_start_time = 0.0
        self.backing_up_final_start_time = 0.0
        self.delay_start_time = 0.0


        #self.drive.back_left.configIntegratedSensorAbsoluteRange(AbsoluteSensorRange.Unsigned_0_to_360)
        #self.encoder = self.drive.back_left.getSensorCollection()        

    def one_note_auto(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.KICKSTAND
            self.arm.shooting_override = False
            print("releasing kickstand")

        elif self.stage == self.KICKSTAND:
            self.arm.desired_position = 95

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 5:
                self.stage = self.MOVING_ARM_1
                print("moving arm")
                self.arm.shooting_override = False   

        elif self.stage == self.MOVING_ARM_1:
            self.arm.desired_position = 16
            
            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 3:
                self.stage = self.REVVING_1
                self.revving_1_start_time = self.timer.getFPGATimestamp()
                self.arm.shooting_override = True

        elif self.stage == self.REVVING_1:
            self.shooter.shooter_spin(1)
            
            if self.revving_1_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING_1
                self.shooting_1_start_time = self.timer.getFPGATimestamp()
                print("shooting")

        elif self.stage == self.SHOOTING_1:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            if self.shooting_1_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.BACKING_UP
                self.backing_up_start_time = self.timer.getFPGATimestamp()
                print("backing up")

        elif self.stage == self.BACKING_UP:
            self.shooter.shooter_spin(0)
            self.intake.intake_spin(0)

            self.drive.tank_drive(0.5, 0.5)

            if self.backing_up_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED
                print("done")

        elif self.stage == self.FINISHED:
            self.drive.tank_drive(0, 0)

        self.arm.arm_to_angle(self.arm.desired_position)


    def two_note_auto(self):
        if self.stage == self.IDLE:
            # perform checks
            self.stage = self.KICKSTAND
            self.arm.shooting_override = False
            print("releasing kickstand")

        elif self.stage == self.KICKSTAND:
            self.arm.desired_position = 95

            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 5:
                self.stage = self.MOVING_ARM_1
                print("moving arm")
                self.arm.shooting_override = False   

        elif self.stage == self.MOVING_ARM_1:
            self.arm.desired_position = 32
            
            if abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 5:
                self.stage = self.DELAY
                self.delay_start_time = self.timer.getFPGATimestamp()
                print("delaying")

        elif self.stage == self.DELAY:
            if self.delay_start_time + 1 < self.timer.getFPGATimestamp() and abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 6:
                self.stage = self.REVVING_1
                self.revving_1_start_time = self.timer.getFPGATimestamp()
                print("revving")

        elif self.stage == self.REVVING_1:
            self.shooter.shooter_spin(0.5)
            self.arm.shooting_override = True

            
            if self.revving_1_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING_1
                self.shooting_1_start_time = self.timer.getFPGATimestamp()
                print("shooting")

        elif self.stage == self.SHOOTING_1:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            self.arm.shooting_override = True

            if self.shooting_1_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.DROPPING_ARM
                print("dropping arm")

        elif self.stage == self.DROPPING_ARM:
            self.arm.desired_position = -13

            self.arm.shooting_override = False

            self.shooter.shooter_spin(0)
            self.intake.intake_spin(0)

            if abs(self.arm.get_arm_pitch()) <= 5:
                self.stage = self.BACKING_UP
                self.backing_up_start_time = self.timer.getFPGATimestamp()
                print("backing up")

        elif self.stage == self.BACKING_UP:
            self.arm.desired_position = -13

            self.shooter.shooter_spin(0)
            self.intake.intake_spin(1)

            self.drive.tank_drive(0.5, 0.5)

            if self.backing_up_start_time + 0.5 < self.timer.getFPGATimestamp():
                self.stage = self.MOVING_ARM_2
                print("moving arm second note")
        
        elif self.stage == self.MOVING_ARM_2:
            self.shooter.shooter_spin(0)
            self.intake.intake_spin(0)

            self.arm.shooting_override = False

            self.arm.desired_position = 35

            if abs(self.arm.get_arm_pitch() - self.arm.desired_position) < 5:
                self.stage = self.DELAY_2
                self.delay_2_start_time = self.timer.getFPGATimestamp()
                print("delaying")

        elif self.stage == self.DELAY_2:
            if self.delay_2_start_time + 1 < self.timer.getFPGATimestamp() and abs(self.arm.desired_position - self.arm.get_arm_pitch()) < 5:
                self.stage = self.REVVING_2
                self.revving_2_start_time = self.timer.getFPGATimestamp()
                print("revving second note")

        elif self.stage == self.REVVING_2:
            self.shooter.shooter_spin(0.5)
            self.arm.shooting_override = True

            if self.revving_2_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.SHOOTING_2
                self.shooting_2_start_time = self.timer.getFPGATimestamp()
                print("shooting second note")

        elif self.stage == self.SHOOTING_2:
            self.shooter.shooter_spin(1)
            self.intake.intake_spin(1)

            self.arm.shooting_override = True

            if self.shooting_2_start_time + 1.5 < self.timer.getFPGATimestamp():
                self.stage = self.BACKING_UP_FINAL
                self.backing_up_final_start_time = self.timer.getFPGATimestamp()
                print("backing up final")

        elif self.stage == self.BACKING_UP_FINAL:
            self.shooter.shooter_spin(0)
            self.intake.intake_spin(0)

            self.drive.tank_drive(0.5, 0.5)

            if self.backing_up_final_start_time + 1 < self.timer.getFPGATimestamp():
                self.stage = self.FINISHED
                print("finished auto")

        elif self.stage == self.FINISHED:
            self.drive.tank_drive(0, 0)

        self.arm.arm_to_angle(self.arm.desired_position)