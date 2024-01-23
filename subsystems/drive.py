# import the helper math functions we are using
from utils import math_functions

# create our Drive class that contains methods for various modes of driving
class Drive:
    def __init__(self, _front_right, _front_left, _back_left, _back_right):
        # create refrences to our motors from the drive class
        # passed into the Drive class from robot.py
        self.front_right = _front_right
        self.front_left = _front_left
        self.back_left = _back_left
        self.back_right = _back_right

    # sets the motors on the left side of our robot to the same speed
    def set_left_speed(self, speed):
        self.front_left.set(speed)
        self.back_left.set(speed)

    # sets the motors on the right side of our robot to the same speed
    def set_right_speed(self, speed):
        self.front_right.set(speed)
        self.back_right.set(speed)

    # spins the motors on the left and right side of our motor based on two joystick values
    # literally how a tank drives just google it lmao
    def tank_drive(self, left_joystick, right_joystick):
        self.set_left_speed(left_joystick)
        self.set_right_speed(right_joystick)

    # Evan coded this on Saturday 1/20
    # behaves the same as arcade drive
    # based on two x and y values from the SAME joystick
    def evans_drive(self, x, y):
        # calculates the speed the motors on the left and right sides of the robot need
        left_speed = y+x
        right_speed = y-x

        # halves the speed for the left and right sides
        left_speed = left_speed*0.5
        right_speed = right_speed*0.5

        # spins the left and right side motors
        self.set_left_speed(left_speed)
        self.set_right_speed(right_speed)