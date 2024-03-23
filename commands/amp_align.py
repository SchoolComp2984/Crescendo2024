from subsystems.drive import Drive
from subsystems.networking import NetworkReciever

class AmpAlign:
    def __init__(self, _drive : Drive, _networking : NetworkReciever):
        self.drive = _drive
        self.networking = _networking

        self.IDLE = 0
        self.MOVING = 1
        self.FINISHED = 2
        self.stage = self.IDLE

    def amp_align(self):
        if self.stage == self.IDLE:
            self.stage = self.MOVING

        elif self.stage == self.MOVING:
            apriltag_data = self.networking.get_apriltag_data()

            sees_apriltag = apriltag_data[4]

            if not sees_apriltag:
                return
            
            apriltag_id = apriltag_data[3]

            if not (apriltag_x == 4 or apriltag_x == 8):
                return

            apriltag_x = apriltag_data[0]

            if abs(apriltag_x) < 20:
                self.stage = self.FINISHED
 
            else:
                if apriltag_x < -20:
                    self.drive.mecanum_drive_robot_oriented(-0.2, 0, 0)
                elif apriltag_x > 20:
                    self.drive.mecanum_drive_robot_oriented(0.2, 0, 0)

        elif self.stage == self.FINISHED:
            self.drive.tank_drive(0, 0)

