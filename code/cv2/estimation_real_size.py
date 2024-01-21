import cv2
import numpy as np
from object_detector import *

# Load Aruco Detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)



# Load Object Detector
detector = HomogeneousBgDetector()

# Load Image
# img = cv2.imread('C:/Users/MIngsu/Desktop/e5b5286dcca2f4e327dcd2db1c322a82.jpg')
img = cv2.imread('G:/mingsu/custom_code/cv2/phone_aruco_marker.jpg')

# Get Aruco marker
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
print(corners)

int_corners = np.int0(corners)

# Draw polygon around the marker
cv2.polylines(img, int_corners, True, (0,255,0), 5)

# Aruco Perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)
print(aruco_perimeter)

# Pixel to cm ratio
pixel_cm_ratio = aruco_perimeter / 20
print(f'pixel2cm : {round(pixel_cm_ratio, 2)}')

contours = detector.detect_objects(img)

# Draw object boundaries
for cnt in contours:

    # Draw polygon
    rect = cv2.minAreaRect(cnt)
    # cv2.polylines(img, [cnt], True, (255,0,0), 3)

    # Get rect
    (x,y), (w,h), angle = rect

    # Get Width and Height of the Objects by applying the Ratio pixel to cm
    object_widht = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio

    # Display rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255,0,0), 3)
    cv2.putText(img, f"Width : {round(object_widht,1)}cm", (int(x),int(y-15)), cv2.FONT_HERSHEY_PLAIN, 2, (100,100,0), 2)
    cv2.putText(img, f"Height : {round(object_height, 1)}cm", (int(x), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 100, 0), 2)

    print(box)

cv2.imshow('Image', img)
cv2.waitKey(0)