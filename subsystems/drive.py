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
        speed_multiplier = 0.5
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

    #field oriented drive
    #same mecanum drive train except the drive is no longer robot-oriented and is field-oriented
    #forwards = moves towards other side of field not in front of the robot
    def field_oriented_drive(self, joystick_x, joystick_y, rotation):
        #gets angle of the robot compared to the true forwards that was set. stores it in the variable
        robot_angle_in_degrees = self.imu.get_yaw()

        #takes angle and converts into radians
        robot_angle_in_radians = robot_angle_in_degrees*math.pi/180

        #resets the direction that we use as the true forwards
        #random key that we'll never randomly press
        #if(self.controller.get)

        #rotates joystick values based on what angle the robot is at
        rotated_x = joystick_x*math.cos(-robot_angle_in_radians)-joystick_y*math.sin(-robot_angle_in_radians)
        rotated_y = joystick_x*math.sin(-robot_angle_in_radians)+joystick_y*math.cos(-robot_angle_in_radians)

        #going side to side has friction so multiply by 1.1 to account for that
        joystick_x = joystick_x*1.1

        #caluculates the speed that each motor needs to have and makes sure that it's between [-1,1]
        maximum_value_of_joysticks = abs(joystick_x)+abs(joystick_y)+abs(rotation)
        scale_factor = max(maximum_value_of_joysticks,1)
        front_left_speed = (rotated_y+rotated_x+rotation)/scale_factor
        back_right_speed = (rotated_y+rotated_x-rotation)/scale_factor
        back_left_speed = (rotated_y-rotated_x+rotation)/scale_factor
        front_right_speed = (rotated_y-rotated_x-rotation)/scale_factor
        
        #since we're testing the robot inside, we don't want it to go full speed, so the motors are multiplied by a decimal
        multiplier = 0.6
        front_left_speed = front_left_speed*multiplier
        front_right_speed = front_right_speed*multiplier
        back_left_speed = back_left_speed*multiplier
        back_right_speed = back_right_speed*multiplier
        
        #these variables set the speed of the robot
        self.front_left.set(front_left_speed)
        self.front_right.set(front_right_speed)
        self.back_left.set(back_left_speed)
        self.back_right.set(back_right_speed)
