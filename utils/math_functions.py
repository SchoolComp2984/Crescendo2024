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
