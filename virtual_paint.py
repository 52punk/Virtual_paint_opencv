#######################################################################
#######################    Virtual Paint   t###########################
#######################################################################


########### This proect is done using OpenCV and Numpy ################

import cv2
import numpy as np
framewidth = 640      # Width and height of the video captured
frameheight = 480

cap = cv2.VideoCapture(0) # Capturing from my Laptop's webcam

cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10, 150)          # Brightness

# The Color Codes which we are going to use
# The Color code is in HSV format

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter('output_1.avi', fourcc, 20.0, (640,480))

myColors = [[0, 145, 130, 31, 255, 255],
            [130, 55, 87, 164, 255, 255],
            [18, 79, 167, 44, 255, 255],
            [51, 58, 116, 82, 255, 255]]

# The Solid colors in BGR format 

myColorValues = [[5,98,249], #BGR format
                 [95,12,83],
                 [3,255,255],
                 [5,230,12]]

def nothing(x):
    pass

cv2.namedWindow("Tracking")
cv2.createTrackbar("Radius", "Tracking", 0, 20, nothing)

# List taken for drawing purpose



myPoints = [] #[x, y, colorId]


def findColor(img, myColors, myColorValues, rad):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)               # Transforming from BGR to HSV format to ease our work
    count = 0                                                   # Refer line 64 and 74
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])                            # Retrieving the Lower bound from myColors
        upper = np.array(color[3:6])                            # Retrieving the Upper bound from myColors
        
        # Creating a mask where we differentiate the object from the surrounding
        mask = cv2.inRange(imgHSV,lower,upper)                 
        
        
        
         # Calling the getContour function to get the Corner Points, 
         # return values are the dimension from where the color will get released
        x,y = getContours(mask)                                 
       
        cv2.circle(imgResult,(x,y),rad,myColorValues[count],cv2.FILLED)  
        
        # making a circle on the tip of the pen which will be coloured by the same color of the pen
        # imgResult is the frame where the actin is being performed
        # x,y are the dimensions in the frame
        # 10 is the radius of the circle
        # myColorValues[count] - we get the count value by the iteration number and then refer to the solid color
        # cv2.FILLED - function to keep the color Filled
        
        
        # For no zero values of x and y newPoints list gets appended by the dimensions and the count referring to the color
        if x!=0 and y!=0:
            newPoints.append([x,y,count,rad])
        count += 1
        #cv2.imshow(str(color[0]),mask)
        
        
        #Reuturnig the newPoints
    return newPoints
        

# Functions to get the corners of the masked frame

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # img is the frame from where we retrieve Extreme outer contours
    
    # initializing x,y,w and h 
    x,y,w,h = 0,0,0,0
    
    # Calculating the areas for each contoured object
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        # Using this condition so that we consider a larger area contour
        if area>500:
           # cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)      # Calculating the perimeter
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True) 
            x, y, w, h = cv2.boundingRect(approx) # Bounding the corners of the object
            
            # returning the dimensions of the tip of the pen
    return x+y//2,y 



# Function to draw on the canvas; giving myPoints list and myColorValues list

def drawOnCanvas(myPoints, myColorValues, rad):
    for point in myPoints:
        
        # Making the circle on the frame(canvas) using the parameters
        # point[0] --> x dimension
        # point[1] --> y dimension
        # point[2] --> colorId, done on myResult frame
        cv2.circle(imgResult,(point[0],point[1]),rad,myColorValues[point[2]],cv2.FILLED)



# Code to start Video capture


while True:
    success, img = cap.read()                             # It ensures that webcam is getting frames
    imgResult = img.copy() 
    imgResult = cv2.flip(imgResult,1)                               # Copy of each frame(image) where the drawing is done
    rad = cv2.getTrackbarPos("Radius", "Tracking")
    newPoints = findColor(imgResult, myColors, myColorValues, rad)   # Retrieving the new points by calling function
    
    # The retrieved newPoints are appended in myPoints list
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
            
    # As we have points in myPoints, we are calling function drawOnCanvas to make the circles on the frames        
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues, rad)
        
    cv2.imshow("Result", imgResult)                       # Displaying the frames
    
    if success == True:
    
     
     
      out.write(imgResult)
      
   
    if cv2.waitKey(1) & 0xFF == ord("q"):                 # For exitting from videocapture
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()