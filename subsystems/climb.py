#Class for the robot's climb system
#Falcon 500 motors
class Climb:
    def __init__(self, _climb_motor_left, _climb_motor_right):
        #creating references to the two climbing motors
        #one motor on each side possibly.
        self.climb_motor_left = _climb_motor_left
        self.climb_motor_right = _climb_motor_right

    def climb_spin(self, speed):
        #basic code to spin the two motors on the climb mechanism.
        self.climb_motor_left.set(speed)
        self.climb_motor_right.set(speed)
    