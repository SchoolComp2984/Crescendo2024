# import opencv, library for real-time computer vision
import cv2

# import numpy and call it np
# allows for better support with arrays and complex mathematical operations
import numpy as np

video = cv2.VideoCapture(0)


while True:
    # get the current frame and store it in variable frame
    # ret is a boolean for if a frame has been grabbed or not
    ret, frame = video.read()
    # cv2.inRange() returns white binary image where colors are detecqted
    hsv_vid = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    #lower_range = () 632514
    lower_range = (99, 67, 80)
    # upper range of red color in HSV
    #upper_range = (30,81,251)
    upper_range = (255, 255, 255) #49302d
    mask = cv2.inRange(hsv_vid, lower_range, upper_range)
    color_video = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the color of the image
    cv2.imshow('Coloured vid', color_video)
    cv2.waitKey(1)
    # cv2.destroyAllWindows()

    # show the current frame in a window called Note Detection
    cv2.imshow("Note Detection", frame)
    

    # if a key has been pressed AND that key is "q", break from the loop/stop reading from the camera
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# closes the IO device for reading from our camera
video.release()

# destroys the window "Note Detection" that has been displaying our video output
cv2.destroyAllWindows()