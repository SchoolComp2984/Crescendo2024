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
    
# interpolation function for our joystick to give a non-linear joystick curve
def interpolation(value):
    pass