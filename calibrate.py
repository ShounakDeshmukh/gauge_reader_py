import cv2
import numpy as np
from utils import detect_circles,visualize_circles,get_value

import time
time.sleep(3) # Sleep for 3 seconds


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
            print("Frame captured")
            break
        
    # Release the camera and close the OpenCV window
    camera.release()
    cv2.destroyAllWindows()


center,radius= detect_circles(frame)

img_marked = visualize_circles(frame,center,radius)

cv2.imwrite("calibration-gauge.png",img_marked)

print("Calibration image saved please refer to it for the next section")

reading1 =int( input("Give the reading on gauge which most closely matches the markings drawn ideally the minimum value of guage"))
angle1 =int( input("give the angle associated with the reading you gave above (the number on marking)"))
reading2 =int( input("give another reading ideally the max reading of gauge"))
angle2 =int( input("give the angle associated with this reading"))
min_reading =int( input("give the minimum reading of the gauge"))
max_reading =int( input("give the maximum reading of the gauge"))

reading_per_degree,angle_at_min=get_value(reading1,angle1,reading2,angle2,min_reading,max_reading)



np.save('calibrated_vars.npy', [center[0],center[1], reading_per_degree, angle_at_min])

print("Calibration done :)")