import cv2
import numpy as np


# constans
lowerh = 0
lowers = 114
lowerv = 168
upperh = 59
uppers = 220
upperv = 213

cap = cv2.VideoCapture("videos/video4.mkv")
lower_color = np.array([lowerh,lowers,lowerv])
upper_color = np.array([upperh, uppers, upperv])

if cap.isOpened() == False:
    print("Error")
else:
    while True:
        ret, frame = cap.read()
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_hsv, lower_color, upper_color)
        blur = cv2.GaussianBlur(mask, (5,5), 0)

        contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contours, -1, (0,0,255), thickness=1)
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
                    #if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    sum_cX += cX
                    sum_cY += cY
                    cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 1)

                final_cX = int(sum_cX/len(contours))
                final_cY = int(sum_cY/len(contours))

                cv2.circle(frame, (final_cX, final_cY), 7, (255,0,0), -1)
                cv2.putText(frame, "center", (final_cX-20, final_cY-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            cv2.putText(frame, (str(len(contours))+" contours"), (25,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            cv2.imshow("Video", frame)
            cv2.imshow("Masked", mask)
        else:
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
cv2.destroyAllWindows()