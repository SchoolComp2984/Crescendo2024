from subsystems.imu import IMU
from utils.pid import PID
class Arm:
    def __init__(self, _arm_motor_left, _arm_motor_right, _arm_imu):
        self.arm_motor_left = _arm_motor_left
        self.arm_motor_right = _arm_motor_right
        self.arm_imu = _arm_imu
    
    def reset_arm_angle(self):
        pass

    def get_arm_angle(self):
        return self.arm_imu.get_pitch()
    
    def move_arm_to_angle(self, _final_angle):
        self.current_angle = self.arm_imu.get_yaw()
        self.final_angle = _final_angle
        #use a pid to get the power needed for the motorpower that we need
        self.motor_power = self.pid.keep_integral(self.final_angle-self.current_angle)