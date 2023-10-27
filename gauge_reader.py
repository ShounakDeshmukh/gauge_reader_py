import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import dist_2_pts

loaded_data = np.load('calibrated_vars.npy')
center = (loaded_data[0],loaded_data[1])
reading_per_degree = loaded_data[2]
angle_at_min = loaded_data[3]
# Check the loaded values

camera = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

if not camera.isOpened():
    print("Error: Could not access the camera.")
else:
    while True:
        
        ret, frame = camera.read()

        if not ret:
            print("Error: Could not capture a frame.")
            break

        
        cv2.imshow("Live Video Stream", frame)

        
        key = cv2.waitKey(1) & 0xFF

        # Press 'c' to capture the current frame
        if key == ord('c'):
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply any necessary preprocessing (e.g., smoothing and thresholding) to enhance contours
        # For example, you can apply Gaussian blur and thresholding:
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

        # Find and detect contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        least_dist = 50
        dist_thresh = 30
        # Iterate through the detected contours
        needle = None


        for contour in contours:
            for point in contour:
                t = dist_2_pts(center[0],center[1],point[0][0],point[0][1])
                if t<least_dist:
                    least_dist = t
                    needle = contour
                    break
            
        # cv2.drawContours(image, needle, -1, (0, 255, 0), 2)

        # rows,cols = image.shape[:2]
        vx,vy,x,y = cv2.fitLine(needle, cv2.DIST_L2,0,0.01,0.01)
        # cv2.line(image,(center[0],center[1]),(int(x),int(y)),(0,0,255),2)

        res = np.arctan2(center[1]-y, center[0]-x)
        # print(res)
        res = np.rad2deg(res) +90
        # print(res)

        reading =(res-angle_at_min)*reading_per_degree
        print(f"{reading} degrees")

    # Release the camera and close the OpenCV window
    camera.release()
    cv2.destroyAllWindows()
