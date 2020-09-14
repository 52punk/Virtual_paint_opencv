import cv2
import numpy as np

cap = cv2.VideoCapture(0);

def nothing(x):
    pass

# trackbars

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
   # frame = cv2.imread('images.jpg')
    
    _, frame = cap.read()
   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    l_h = cv2.getTrackbarPos("LH", "Tracking") # lower hue
    l_s = cv2.getTrackbarPos("LS", "Tracking") # lower saturation
    l_v = cv2.getTrackbarPos("LV", "Tracking") # lower value
    
    u_h = cv2.getTrackbarPos("UH", "Tracking") # upper hue
    u_s = cv2.getTrackbarPos("US", "Tracking") # upper saturation
    u_v = cv2.getTrackbarPos("UV", "Tracking") # upper value
    
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    
    mask = cv2.inRange(hsv, l_b, u_b)
    
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    cv2.imshow("frame", frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()