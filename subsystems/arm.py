#importing libraries
import phoenix5
import rev

#importing IMU function to use the yaw of the arm for moving it to a certain angle
from subsystems.imu import IMU

#importing the PID for moving the arm to the right place.
from utils.pid import PID

# import our clamp function
from utils.math_functions import clamp

class Arm:
    #initiating the arm values and stuff
    def __init__(self, _arm_motor_left_front, _arm_motor_left_back, _arm_motor_right_front, _arm_motor_right_back, _arm_imu):
        #references to the arm motors and the imu that were passed in.
        self.arm_motor_left_front = _arm_motor_left_front
        self.arm_motor_left_back = _arm_motor_left_back

        self.arm_motor_right_front = _arm_motor_right_front
        self.arm_motor_right_back = _arm_motor_right_back

        self.arm_imu = _arm_imu

        #proportional constant, integral constant, derivative constand for pid
        #numbers are placeholders for now. 
        self.arm_p = 0.05
        self.arm_i = 0
        self.arm_d = 0
        #make previous error zero
        self.arm_val = 0

        #setting up the PIDS for the arm
        self.arm_pid = PID(self.arm_p, self.arm_i, self.arm_d, self.arm_val)
    
    def set_speed(self, speed):
        self.arm_motor_left_front.set(speed)
        self.arm_motor_left_back.set(speed)

        self.arm_motor_right_front.set(speed)
        self.arm_motor_right_back.set(speed)


    #i believe that if we are to put an IMU on the arm, it would be best to have it lay on the horizontal side of the arm so that we can just use the yaw to measure the angle.
    #function to reset yaw of the arm IMU
    def reset_arm_angle(self):
        self.arm_imu.reset_pitch()

    #function to get the angle (pitch) of the arm
    def get_arm_pitch(self):
        return self.arm_imu.get_pitch()
    
    # function to stop spinning the arm motors
    def stop(self):
        self.arm_motor_left_front.set(0)
        self.arm_motor_left_back.set(0)

        self.arm_motor_right_front.set(0)
        self.arm_motor_right_back.set(0)

    def move_arm_to_angle(self, desired_angle):
        #references to the current angle that is passsed in and the final angle that we need.
        current_angle = self.get_arm_pitch()
        desired_angle = desired_angle

        # calculate the error that we pass into the PID controller
        error = desired_angle - current_angle

        #use a pid to get the power needed for the motorpower that we need
        pid_adjustment = self.arm_pid.keep_integral(error)
        
        # clamp our PID adjustment between relatively small values for testing
        pid_adjustment = clamp(pid_adjustment, -0.20, 0.20)

        print(f"pid adjustment: {pid_adjustment}")

        #spin the motors based on calculated PID value
        #test this! motors may spin opposite directions
        self.set_speed(pid_adjustment)
    
    