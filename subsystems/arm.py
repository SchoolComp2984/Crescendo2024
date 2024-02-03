from subsystems.imu import IMU
from utils import pid
import phoenix5
import rev
class Arm:
    def __init__(self, _arm_motor_left, _arm_motor_right, _arm_imu, _pid: pid.PID):
        self.arm_motor_left = _arm_motor_left
        self.arm_motor_right = _arm_motor_right
        self.arm_imu = _arm_imu

        #proportional constant, integral constant, derivative constand for pid
        #numbers are placeholders for now. 
        self.arm_p = .25
        self.arm_i = .1
        self.arm_d = .05
        #make previous error zero
        self.arm_val = 0

        #setting up the PIDS for each arm motor.
        self.arm_motor_left_pid = pid.PID()
        self.arm_motor_left_pid.set_pid(self.arm_p, self.arm_i, self.arm_d, self.arm_val)

        self.arm_motor_right_pid = pid.PID()
        self.arm_motor_right_pid.set_pid(self.arm_p, self.arm_i, self.arm_d, self.arm_val)
    
    #i believe that if we are to put an IMU on the arm, it would be best to have it lay on the horizontal side of the arm so that we can just use the yaw to measure the angle.
    #function to reset yaw of the arm IMU
    def reset_arm_angle(self):
        self.arm_imu.reset_yaw()

    #function to get the yaw of the arm
    def get_arm_yaw(self):
        return self.arm_imu.get_yaw()

    def get_arm_pitch(self):
        return self.arm_imu.get_pitch()

    def move_arm_to_angle(self, _current_angle, _final_angle):
        #references to the current angle that is passsed in and the final angle that we need.
        self.current_angle = _current_angle
        self.final_angle = _final_angle

        #use a pid to get the power needed for the motorpower that we need
        self.arm_motor_left_pid = self.arm_motor_left_pid.keep_integral(self.final_angle - self.current_angle)
        self.arm_motor_right_pid = self.arm_motor_right_pid.keep_integral(self.final_angle - self.current_angle)
        self.arm_motor_left.set(self.arm_motor_left_pid)
        self.arm_motor_right.set(self.arm_motor_right_pid)
    
    #unsure if we need a manual arm moving function
    