# import math to use trig functions and PI
import math

# create our Drive class that contains methods for various modes of driving
class Drive:
    def __init__(self, _front_right, _front_left, _back_left, _back_right, _imu):
        # create refrences to our motors from the drive class
        # passed into the Drive class from robot.py
        self.front_right = _front_right
        self.front_left = _front_left
        self.back_left = _back_left
        self.back_right = _back_right

        # create reference to our imu which is passed into our Drive class from robot.py
        self.imu = _imu

    # sets the motors on the left side of our robot to the same speed
    def set_left_speed(self, speed):
        self.front_left.set(speed)
        self.back_left.set(speed)

    # sets the motors on the right side of our robot to the same speed
    def set_right_speed(self, speed):
        self.front_right.set(speed)
        self.back_right.set(speed)


    # Evan coded this on Saturday 1/20
    # behaves the same as arcade drive
    # based on two x and y values from the SAME joystick
    def evans_drive(self, x, y):
        # calculates the speed the motors on the left and right sides of the robot need
        left_speed = y+x
        right_speed = y-x

        # halves the speed for the left and right sides
        # too fast to be testing indoors
        left_speed = left_speed*0.5
        right_speed = right_speed*0.5

        # spins the left and right side motors
        self.set_left_speed(left_speed)
        self.set_right_speed(right_speed)

    # drivetrain that allows the robot to move forward/backward, sideways (strafing), and rotating in place
    # left joystick x and y for f/b/l/r and right joystick x for turning in place
    # coded by Aram on Tuesday 1/23
    # https://gm0.org/en/latest/docs/software/tutorials/mecanum-drive.html
    def mecanum_drive_robot_oriented(self, joystick_x, joystick_y, joystick_turning):
        # calculate speed of front left and back right motors
        # similar to arcade drive
        # these motors spin with the same speed
        front_left_speed = joystick_y + joystick_x + joystick_turning
        back_right_speed = joystick_y + joystick_x - joystick_turning

        # calculate speed of front right and back left motors
        # spin in same direction, same y as motors above, but different sign on the x
        front_right_speed = joystick_y - joystick_x - joystick_turning
        back_left_speed = joystick_y - joystick_x + joystick_turning

        # scale the speeds back into our [-1,1] range
        # gonna be the max between all joystick values and 1
        motor_power_sum = abs(joystick_y) + abs(joystick_x) + abs(joystick_turning)
        scale_back_to_range = max(motor_power_sum, 1)
        
        # divide all motor speeds by scale
        front_right_speed /= scale_back_to_range
        front_left_speed /= scale_back_to_range
        back_left_speed /= scale_back_to_range
        back_right_speed /= scale_back_to_range

        # multiply all motor speeds by speed multiplier
        speed_multiplier = 0.1
        front_right_speed *= speed_multiplier
        front_left_speed *= speed_multiplier
        back_left_speed *= speed_multiplier
        back_right_speed *= speed_multiplier

        # actually spin the motors
        # ordered the same as CAN device IDs
        self.front_right.set(front_right_speed)
        self.front_left.set(front_left_speed)
        self.back_left.set(back_left_speed)
        self.back_right.set(back_right_speed)



        
 