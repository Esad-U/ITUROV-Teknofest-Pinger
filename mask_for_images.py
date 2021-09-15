import cv2
import os
import numpy as np

lowerh = 0
lowers = 114
lowerv = 168
upperh = 59
uppers = 189
upperv = 213

def nothing(x):
    pass
font = cv2.FONT_HERSHEY_SIMPLEX


cv2.namedWindow("Settings")

cv2.createTrackbar("Lower-Hue", "Settings", 0, 180, nothing)
cv2.createTrackbar("Lower-Saturation", "Settings", 0, 255, nothing)
cv2.createTrackbar("Lower-Value", "Settings", 0, 255, nothing)
cv2.createTrackbar("Upper-Hue", "Settings", 0, 180, nothing)
cv2.createTrackbar("Upper-Saturation", "Settings", 0, 255, nothing)
cv2.createTrackbar("Upper-Value", "Settings", 0, 255, nothing)

images = os.listdir()
for i in images:
    if i.endswith("jpg") or i.endswith("JPG") or i.endswith("jpeg"):
        print(i)
        image = cv2.imread(i)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        while True:
            lh = cv2.getTrackbarPos("Lower-Hue", "Settings")
            ls = cv2.getTrackbarPos("Lower-Saturation", "Settings")
            lv = cv2.getTrackbarPos("Lower-Value", "Settings")
            uh = cv2.getTrackbarPos("Upper-Hue", "Settings")
            us = cv2.getTrackbarPos("Upper-Saturation", "Settings")
            uv = cv2.getTrackbarPos("Upper-Value", "Settings")

            lower_color = np.array([lh, ls, lv])
            upper_color = np.array([uh, us, uv])

            mask = cv2.inRange(hsv, lower_color, upper_color)

            cv2.imshow("image", image)
            cv2.imshow("mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

cv2.destroyAllWindows()
