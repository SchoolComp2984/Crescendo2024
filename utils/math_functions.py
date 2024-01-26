# clamps a value between a minimum and maximum value
# if larger than the max, use the max
# if smaller than the min, use the min
# otherwise, use the original value
def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

#interpolation function to take the linear joystick positions into a piecewise curve
#if between certain values, return a certain value for the joystick
#makes the drive less sensitive overall to prevent random jerks when the joystick moves
def interpolation_drive(value):
    #gets the absolute value
    value_abs = abs(value)
    #if abs of the value is less than .14, set the value to 0 to
    #prevent the robot from moving when the joystick is supposed to be neutral
    if value_abs<.14: return 0
    #if under .65, return .33
    elif value_abs<.65: return .33
    #if under .9, return .6
    elif value_abs<.9: return .66
    #if it's normal, return 1. Full speed
    else: return 1

"""
      def steer_pid(self, error):
            adjustment(p term) = error * self.p   
            if self.integral > 0 and (error * self.i < 0): if over, start over but go down
                  self.integral = 0
            if (self.integral < 0) and (error * self.i > 0): if under, start over and go up
                  self.integral = 0
            self.integral += error*self.i      
            if (-20 < error) and (error < 20):
                  adjustment += self.integral
            else: 
                  self.integral=0
            adjustment += (error - self.previous_input) * self.d
            self.previous_input = error
            return adjustment
            """