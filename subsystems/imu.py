# import phoenix5 library because we need the phoenix5._ctre.sensors.PigeonIMU
# using the IMU to return gyroscope values
import phoenix5

# create IMU class of type PigeonIMU
class IMU(phoenix5._ctre.sensors.PigeonIMU):
    # initialize class and get properties from parent motor controller class
    def __init__(self, _parent_motor_controller : phoenix5._ctre.WPI_TalonSRX):
        super().__init__(_parent_motor_controller)

    # return the yaw of our robot (using this the most)
    # return unit is degrees
    def get_yaw(self):
        return self.getYawPitchRoll()[1][0]
    
    def reset_yaw(self):
        self.reset

    # check if our IMU has "waken up" and is ready to be used
    def is_ready(self):
        # check if the state of the IMU is ready
        # means that it is ready to be used
        if self.getState() == phoenix5._ctre.sensors.PigeonIMU.PigeonState.Ready:
            # return True if it is ready
            return True
        # if it is anything except ready, we should not use it so return False
        return False