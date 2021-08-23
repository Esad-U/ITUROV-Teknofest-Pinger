import cv2
import numpy as np


# constans
lowerh = 0
lowers = 114
lowerv = 168
upperh = 59
uppers = 220
upperv = 213

def yaw_right(image):
    cv2.putText(image, "Yaw Right", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
def yaw_left(image):
    cv2.putText(image, "Yaw Left", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
def ascend(image):
    cv2.putText(image, "Go Up", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
def descend(image):
    cv2.putText(image, "Go Down", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


cap = cv2.VideoCapture("videos/video4.mkv")
lower_color = np.array([lowerh,lowers,lowerv])
upper_color = np.array([upperh, uppers, upperv])

if cap.isOpened() == False:
    print("Error")
else:
    while True:
        ret, frame = cap.read()
        # center of frame
        center_y = int(frame.shape[0]/2)
        center_x = int(frame.shape[1]/2)
        # line constants
        x_blank = 120
        y_blank = 80
        color = (255,255,0)
        # border lines
        vert_line_left = center_x - x_blank
        vert_line_right = center_x + x_blank
        horiz_line_bot = center_y + y_blank
        horiz_line_top = center_y - y_blank
        cv2.line(frame, (vert_line_left, 0), (vert_line_left, frame.shape[0]), color, 1)
        cv2.line(frame, (vert_line_right, 0), (vert_line_right, frame.shape[0]), color, 1)
        cv2.line(frame, (0, horiz_line_top), (frame.shape[1], horiz_line_top), color, 1)
        cv2.line(frame, (0, horiz_line_bot), (frame.shape[1], horiz_line_bot), color, 1)

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_hsv, lower_color, upper_color)
        blur = cv2.GaussianBlur(mask, (5,5), 0)

        contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if ret:
            if len(contours) > 0:
                """if len(contours) > 1:
                    cnt = contours[int(len(contours)/2)]
                elif len(contours) == 1:
                    cnt = contours[0]"""

                sum_cX = 0
                sum_cY = 0
                for cnt in contours:
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        sum_cX += cX
                        sum_cY += cY
                        cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 1)

                final_cX = int(sum_cX/len(contours))
                final_cY = int(sum_cY/len(contours))

                cv2.circle(frame, (final_cX, final_cY), 7, (255,0,0), -1)
                cv2.putText(frame, "center", (final_cX-20, final_cY-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                if final_cX < vert_line_left:
                    yaw_left(frame)
                elif final_cX > vert_line_right:
                    yaw_right(frame)
                if final_cY < horiz_line_top:
                    ascend(frame)
                elif final_cY > horiz_line_bot:
                    descend(frame)

            cv2.putText(frame, (str(len(contours))+" contours"), (25,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            cv2.imshow("Video", frame)
            cv2.imshow("Masked", blur)
        else:
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
cv2.destroyAllWindows()