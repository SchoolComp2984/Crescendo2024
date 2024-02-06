from subsystems.imu import IMU
from utils.pid import PID
import phoenix5
import rev


class Arm:
    def __init__(self, _arm_motor_left, _arm_motor_right, _arm_imu):
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

        #setting up the PIDS for the arm
        self.arm_motor_pid = PID(self.arm_p, self.arm_i, self.arm_d, self.arm_val)
    
    #i believe that if we are to put an IMU on the arm, it would be best to have it lay on the horizontal side of the arm so that we can just use the yaw to measure the angle.
    #function to reset yaw of the arm IMU
    def reset_arm_angle(self):
        self.arm_imu.reset_yaw()

    #function to get the yaw of the arm
    def get_arm_yaw(self):
        return self.arm_imu.get_yaw()

    # returns the pitch of the arm (vertical rotation), which we will probably want to use instead of yaw depending on how we mount the IMU
    def get_arm_pitch(self):
        return self.arm_imu.get_pitch()

    def move_arm_to_angle(self, _current_angle, _desired_angle):
        #references to the current angle that is passsed in and the final angle that we need.
        self.current_angle = _current_angle
        self.desired_angle = _desired_angle

        #use a pid to get the power needed for the motorpower that we need
        self.arm_motor_pid = self.arm_motor_pid.keep_integral(self.desired_angle - self.current_angle)
        
        #spin the motors based on calculated PID value
        self.arm_motor_left.set(self.arm_motor_pid)
        self.arm_motor_right.set(self.arm_motor_pid)
    
    