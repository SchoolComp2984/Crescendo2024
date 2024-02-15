import cv2
# import opencv, library for real-time computer vision
import cv2

# REMEBER TO WRITE ON GOOGLE DOC NOTES - siena :)

# import numpy and call it np
# allows for better support with arrays and complex mathematical operations
import numpy as np

# create an instance of the cv2 class for video capturing from a camera
# 0 is the index of the camera we want to capture from
video = cv2.VideoCapture(0)

# set width and height of our video capture
WIDTH = 300
HEIGHT = 300
video.set(3, WIDTH)
video.set(4, HEIGHT)

# set boundaries for the colors we want to detect
# in HSV
min_orange_1 = (10, 50, 50)
max_orange_1 = (30, 255, 255)

# create a loop to read a new frame from the camera on each iteration
while True:
    # get the current frame and store it in variable frame
    # ret is a boolean for if a frame has been grabbed or not
    ret, frame = video.read()

    # blur our image to improve speed of detection algorithm
    blurred_frame = cv2.GaussianBlur(frame, (7, 7), cv2.BORDER_DEFAULT)

    # convert our blurred frame to HSV from BGR
    hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_RGB2HSV)

    # detect the orange color in our hsv frame
    color_mask = cv2.inRange(hsv_frame, min_orange_1, max_orange_1)
    
    # convert our video stream to grayscale     
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # combine our mask with our grayscale frame
    combined_frame = cv2.bitwise_and(color_mask, grayscale_frame)

    # detect circles from our combined frame
    detected_circles = cv2.HoughCircles(combined_frame, cv2.HOUGH_GRADIENT_ALT, 4, 15, param1=300, param2=0.95, minRadius=0, maxRadius=-1)
    print(detected_circles)
    # check that circles have actually been detected
    if detected_circles is not None:
        # convert detected circles to a usable array
        detected_circles = np.uint16(np.around(detected_circles))
        print("here")
        # iterate through detected circles
        for point in detected_circles[0, :]:
            # get the x and y position of the current circle as well as the radius
            x, y, radius = point[0], point[1], point[2]
            print("here2")
            # draw the circumference of the circle
            cv2.circle(frame, (x, y), radius, (0, 0, 255))

            # make a point for the center of the circle
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 3)

    grayscale_frame = cv2.cvtColor(grayscale_frame, cv2.COLOR_GRAY2BGR)
    finaldif = cv2.absdiff(frame, grayscale_frame)
    cv2.imshow("final dif", finaldif)
    # show the current frame in a window called Note Detection
    cv2.imshow("frame", frame)
    cv2.imshow("blurred", blurred_frame)
    cv2.imshow("hsv", hsv_frame)
    cv2.imshow("colored mask", color_mask)
    cv2.imshow("grayscale frame", grayscale_frame)
    cv2.imshow("combined frame", combined_frame)


    # if a key has been pressed AND that key is "q", break from the loop/stop reading from the camera
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# closes the IO device for reading from our camera
video.release()

# destroys the window "Note Detection" that has been displaying our video output
cv2.destroyAllWindows()