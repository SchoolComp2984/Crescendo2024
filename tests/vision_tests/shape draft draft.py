
import cv2 
import numpy as np 
from matplotlib import pyplot as plt 
  
# Video Object 
vid = cv2.VideoCapture(0)
while True:
    # get the current frame from video object and store it in variable frame
    # ret is a boolean for if a frame has been grabbed or not
    ret, frame = vid.read()

    # attempt to read shaped from a test image (we couldn't get imread() to work)
    #frame = cv2.imread('car.jpeg')
    # print(frame)

    # from last years code to find cube shapes  RaspberryPiCode2023/CubeConeTracker.py
    # TODO: figure out what these functions do, what the parameters are, and how to change them to work better
    #   potentially change the kernel to larger (this is a filter that is applied to a certain 2x2 box of pixels at a time, so 3x3 means 3x3 pixels)
    # TODO: add color-detection code here to filter the image by color before findContours()
    kernel = np.ones((3, 3), np.uint8)
    # inRange() returns a binary image (2x2 array of 0s and 1s) of all the blue, green, and red values (check this order?) that are between the ranges given as parameters
    mask = cv2.inRange(frame, (0, 0, 0), (0, 0, 255))  # play with these values
    eroded_result = cv2.erode(mask, kernel, cv2.BORDER_REFLECT)
    # findContours() is a shape-detection function 
    # contours is a list of contour objects (idk what that is though)
    contours, hier = cv2.findContours(eroded_result,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # color detection code, add this above before findCountours() ?
    # converting image into grayscale image 
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    # setting threshold of gray image 
    #_, threshold = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY) 
    
    # using a findContours() function example from online somewhere
    #contours, _ = cv2.findContours( threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
    # ALL THE CODE BELOW IS FOR PROCESSING AND DISPLAYING THE DETECTED CONTOURS
    # note a circle is defined as a shape with >= 8 edges
    i = 0
    
    # list for storing names of shapes 
    for contour in contours: 
    
        # here we are ignoring first counter because  
        # findcontour function detects whole image as shape 
        if i == 0: 
            i = 1
            continue
    
        # cv2.approxPloyDP() function to approximate the shape 
        approx = cv2.approxPolyDP( 
            contour, 0.01 * cv2.arcLength(contour, True), True) 
        
        # using drawContours() function 
        cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5) 
    
        # finding center point of shape 
        M = cv2.moments(contour) 
        if M['m00'] != 0.0: 
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00']) 
    
        # putting shape name at center of each shape 
        if len(approx) == 3: 
            cv2.putText(frame, 'Triangle', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        elif len(approx) == 4: 
            cv2.putText(frame, 'Quadrilateral', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        elif len(approx) == 5: 
            cv2.putText(frame, 'Pentagon', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        elif len(approx) == 6: 
            cv2.putText(frame, 'Hexagon', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
        else: 
            cv2.putText(frame, 'circle', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    
    # show the current frame in a window called Note Detection
    cv2.imshow("Note Detection", frame)

    # if a key has been pressed AND that key is "q", break from the loop/stop reading from the camera
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# closes the IO device for reading from our camera
vid.release()

# destroys the window "Note Detection" that has been displaying our video output
cv2.destroyAllWindows()