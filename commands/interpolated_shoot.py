from utils.math_functions import interpolation_array

from subsystems.drive import Drive
from subsystems.networking import NetworkReciever

from commands.manual_shoot import ManualShoot

class InterpolatedShoot:
    def __init__(self, _drive : Drive, _manual_shoot : ManualShoot, _networking : NetworkReciever):
        self.IDLE = 0
        self.ALIGNING = 1
        self.SHOOTING = 2
        self.FINISHED = 3
        self.stage = self.IDLE

        self.manual_shoot = _manual_shoot
        self.drive = _drive
        self.networking = _networking

        self.distance = -1

        self.running = False

    def kg_interpolation(self, value):
        arr = [ \
        [0, 20],\
        [8, 60]]

        return interpolation_array(value, arr)

    def interpolated_shoot(self):
        if not self.running:
            return

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
                self.stage = self.SHOOTING

        elif self.stage == self.SHOOTING:
            if not self.manual_shoot.stage == self.manual_shoot.FINISHED:
                angle = self.angle_interpolation(self.distance)

                self.manual_shoot.manual_shoot(angle)
            else:
                self.stage = self.FINISHED

        elif self.stage == self.FINISHED:
            self.running = False

            