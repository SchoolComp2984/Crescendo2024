# import our clamp function
from utils.math_functions import clamp, interpolation_array

# import math for cos functions
import math

class Arm:
    #initiating the arm values and stuff
    def __init__(self, _arm_motor_left_front, _arm_motor_left_back, _arm_motor_right_front, _arm_motor_right_back, _arm_imu):
        #references to the arm motors and the imu that were passed in.
        self.arm_motor_left_front = _arm_motor_left_front
        self.arm_motor_left_back = _arm_motor_left_back

        self.arm_motor_right_front = _arm_motor_right_front
        self.arm_motor_right_back = _arm_motor_right_back

        self.arm_imu = _arm_imu

        # proportional constant
        self.kp = 0.002

        # init gravity compensation
        self.gravity_compensation = 0

        #make previous error zero
        self.arm_val = 0

        # init desired position value
        self.desired_position = 87

        # init shooting override value
        self.shooting_override = False
        self.shooting_holding_value = 0

    def set_speed(self, speed):
        self.arm_motor_left_front.set(speed)
        self.arm_motor_left_back.set(speed)

        self.arm_motor_right_front.set(speed)
        self.arm_motor_right_back.set(speed)

    #function to get the angle (pitch) of the arm
    def get_arm_pitch(self):
        return self.arm_imu.get_pitch() + 87.2314
    
    # function to stop spinning the arm motors
    def stop(self):
        self.arm_motor_left_front.set(0)
        self.arm_motor_left_back.set(0)

        self.arm_motor_right_front.set(0)
        self.arm_motor_right_back.set(0)

    def kg_interpolation(self, value):
      arr = [ \
      [0, 0.17],\
      [34.2, 0.16],\
      [45.5, 0.14],\
      [90, 0.1]]


      return interpolation_array(value, arr)

    def k_down_interpolation(self, value):
        arr = [ \
            [0, 0.008],\
            [15, 0.008],\
            [22.5, 0.007],\
            [30, 0.005],\
            [60, 0.0033],\
            [90, 0.0013]]
        
        return interpolation_array(value, arr)
    
    def arm_to_angle(self, desired_angle):
        if desired_angle < -10 or desired_angle > 90:
            return

        # get our current arm angle
        current_angle = self.get_arm_pitch()

        # calculate the error that we pass into the PID controller
        error = desired_angle - current_angle

        # calculate proportional term
        #pid_value = self.arm_pid.keep_integral(error)

        k = self.kp

        if (error < 0):
            k = self.k_down_interpolation(current_angle)

        proportional = k * error

        # calculate justified current arm angle in radians
        justifed_angle_radians = current_angle * math.pi / 180

        if current_angle < desired_angle - 1 or current_angle > desired_angle + 1:
            self.gravity_compensation = math.cos(justifed_angle_radians) * self.kg_interpolation(current_angle)

        # calculate motor power
        motor_power = self.gravity_compensation + proportional

        # clamp our motor power so we don't move to fast
        motor_power_clamped = clamp(motor_power, -0.05, 0.2)

        # check if not shooting
        if not self.shooting_override:
            self.shooting_holding_value = motor_power_clamped


        #print(f"desired: {self.desired_position}, current: {current_angle}, pow: {motor_power_clamped}")
        #spin the motors based on calculated PID value or previously stored holding value
        if self.shooting_override:
            self.set_speed(self.shooting_holding_value)
        else:
            self.set_speed(motor_power_clamped)
    
    def arm_gravity_test(self, printout):
        # get the current angle from the IMU
        current_angle = self.get_arm_pitch()

         # calculate justified current arm angle in radians
        justifed_angle_radians = current_angle * math.pi / 180

        # calculate gravity compensation
        gravity_compensation = math.cos(justifed_angle_radians) * self.kg_interpolation(current_angle)

        # calculate motor power
        motor_power = clamp(gravity_compensation, -0.2, 0.23)

        # spin motors
        self.set_speed(motor_power)

        if printout:
            print(f"angle: {self.get_arm_pitch()}, kg: {self.kg_interpolation(current_angle)}, motor power: {motor_power}")
