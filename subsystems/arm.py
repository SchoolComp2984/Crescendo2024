#importing libraries
import phoenix5
import rev

#importing IMU function to use the yaw of the arm for moving it to a certain angle
from subsystems.imu import IMU

#importing the PID for moving the arm to the right place.
from utils.pid import PID

# import our clamp function
from utils.math_functions import clamp

# import math
from utils import math_functions

# import math for PID
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
        self.kp = 0.001

        # gravity compensation constant
        self.kg = 0.05

        #make previous error zero
        self.arm_val = 0

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
      [0, 0.25],\
      [34.2, 0.188],\
      [45.5, 0.142],\
      [90, 0.104]]


      return math_functions.interpolation_array(value, arr)

    def arm_to_angle(self, desired_angle):
        # get our current arm angle
        current_angle = self.get_arm_pitch()

        # calculate the error that we pass into the PID controller
        error = desired_angle - current_angle

        # initialize adjustment to 0
        adjustment = 0

        # check if we are within 10 degrees
        if abs(error) > 5:
            adjustment = 0.03


        # check  we are within 20 degrees
        if abs(error) > 10:
            adjustment = 0.05


        # flip adjustent sign if moving up
        if error > 0:
            adjustment = -adjustment

        # calculate justified current arm angle in radians
        justifed_angle_radians = current_angle * math.pi / 180

        # calculate gravity compensation
        gravity_compensation = math.cos(justifed_angle_radians) * self.kg_interpolation(current_angle)

        # calculate motor power
        motor_power = gravity_compensation + adjustment

        # clamp our motor power so we don't move to fast
        motor_power_clamped = clamp(motor_power, -0.2, 0.2)

        print(f"desired: {desired_angle}, angle: {current_angle}, adjustment: {adjustment}, motor power: {motor_power_clamped}")

        #spin the motors based on calculated PID value
        self.set_speed(motor_power_clamped)
    
    def arm_gravity_test(self, printout):
        # get the current angle from the IMU
        current_angle = self.get_arm_pitch()

         # calculate justified current arm angle in radians
        justifed_angle_radians = current_angle * math.pi / 180

        # calculate gravity compensation
        gravity_compensation = math.cos(justifed_angle_radians) * self.kg_interpolation(current_angle)

        # calculate motor power
        motor_power = clamp(gravity_compensation, -0.2, 0.2)

        # spin motors
        self.set_speed(motor_power)

        if printout:
            print(f"angle: {self.get_arm_pitch()}, kg: {self.kg_interpolation(current_angle)}, motor power: {motor_power}")
