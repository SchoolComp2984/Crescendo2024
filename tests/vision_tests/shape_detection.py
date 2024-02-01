# import opencv, library for real-time computer vision
import cv2

# import numpy and call it np
# allows for better support with arrays and complex mathematical operations
import numpy as np

from matplotlib import pyplot as plt 

# create an instance of the cv2 class for video capturing from a camera
# 0 is the index of the camera we want to capture from
video = cv2.VideoCapture(0)

# set boundaries for the colors we want to detect
# cv2 represents colors in BGR (blue, red, green)
# dark: 1, 23, 207     light: 30,81,251
lower_orange = (1, 23, 100)
upper_orange = (30, 80, 255)


# create a loop to read a new frame from the camera on each iteration
while True:
    # get the current frame and store it in variable frame
    # ret is a boolean for if a frame has been grabbed or not
    ret, frame = video.read()
    # cv2.inRange() returns white binary image where colors are detected
    mask = cv2.inRange(frame, lower_orange, upper_orange)

    # instead of having a white mask showing what is detected, show the color from the original frame
    # threshold = cv2.bitwise_and(frame, frame, mask=mask)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) 

    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) 

    # using a findContours() function 
    contours, _ = cv2.findContours( 
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    

    # show the current frame in a window called Note Detection
    cv2.imshow("Note Detection", contours)

    # if a key has been pressed AND that key is "q", break from the loop/stop reading from the camera
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# closes the IO device for reading from our camera
video.release()

# destroys the window "Note Detection" that has been displaying our video output
cv2.destroyAllWindows()