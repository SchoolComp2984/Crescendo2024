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
    #if under .9, return .66
    elif value_abs<.9: return .66
    #if it's normal, return 1. Full speed
    else: return 1

def interpolation_array(value, arr):
      # if value is less than the first number in array, which is -1, set to first corresponding value in array, which is -12
      if value <= arr[0][0]:
            return arr[0][1]

      # if value is greater than the last number in array, which is 1, set to last corresponding value in array, which is 12
      if value >= arr[len(arr) - 1][0]: 
            return arr[len(arr) - 1][1]

      # if it is inside the range from -1 to 1, then see which two value in the array it is in between
      # return some random number idk what it is that corresponds to the range the value is 
      for i in range(len(arr) - 1):
            if ((value>=arr[i+0][0]) and (value<=arr[i+1][0])): 
                  return (value-arr[i+0][0])*(arr[i+1][1]-arr[i+0][1])/(arr[i+1][0]-arr[i+0][0])+arr[i+0][1]
      return 0