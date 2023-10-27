import cv2
import numpy as np
# import matplotlib.pyplot as plt
import math

def dist_2_pts(x, y, x1, y1):
    return math.sqrt((x - x1)**2 + (y - y1)**2)

def detect_circles(image):
    image1 = image.copy()
    gray_image = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 2)
    height, width = blurred_image.shape[:2]
    circles = cv2.HoughCircles(
        blurred_image, cv2.HOUGH_GRADIENT, dp=0.25, minDist=20, param1=100, param2=50, minRadius=int(height * 0.25), maxRadius=int(height * 0.48)
    )

    if circles is not None and len(circles[0]) > 0:
        circle = np.round(circles[0][0]).astype("int")
        center = (circle[0], circle[1])
        radius = circle[2]
        return center, radius
    else:
        return None, None


def visualize_circles(image, center, radius):
    if image is not None and center is not None and radius is not None:
        image_with_circles = image.copy()
        cv2.circle(image_with_circles, center, radius, (0, 255, 0), 2)
        expansion_factor = 1.2
        # x, y = int(center[0] - radius * expansion_factor), int(center[1] - radius * expansion_factor)
        w, h = int(2 * radius * expansion_factor), int(2 * radius * expansion_factor)
        # cropped_circle = image[y:y+h, x:x+w]

        text_scaling_factor = min(w, h) / 200.0
        # font_scale = 0.25 * text_scaling_factor
        font_thickness = int(text_scaling_factor)
        text_positions = []

        num_markings = 72
        for i in range(num_markings):
            angle = i * (360 / num_markings)
            angle_rad = math.radians(angle + 90)
            x1 = int(center[0] + (radius - 10) * math.cos(angle_rad))
            y1 = int(center[1] + (radius - 10) * math.sin(angle_rad))
            x2 = int(center[0] + (radius + 10) * math.cos(angle_rad))
            y2 = int(center[1] + (radius + 10) * math.sin(angle_rad))
            cv2.line(image_with_circles, (x1, y1), (x2, y2), (0, 0, 255), 1)

            text_x = int(center[0] + (radius + 18 * text_scaling_factor) * math.cos(angle_rad))
            text_y = int(center[1] + (radius + 10 * text_scaling_factor) * math.sin(angle_rad))
            text_positions.append((text_x, text_y))

        for i, (text_x, text_y) in enumerate(text_positions):
            cv2.putText(image_with_circles, f"{int(i * (360 / num_markings))}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), font_thickness)

        return  image_with_circles

        # print(f'shape is = {cropped_circle.shape}')
        # print(f'radius is = {radius}')




def get_value(reading1,angle1,reading2,angle2,min_reading,max_reading):

    reading_per_degree = np.float16(abs(reading1-reading2)/abs(angle1-angle2))
    # angle1 = theta + angle_of_min
    angle_at_min = angle1 - ((reading1 - min_reading)/reading_per_degree)
    print(reading_per_degree,angle_at_min)

    return reading_per_degree,angle_at_min