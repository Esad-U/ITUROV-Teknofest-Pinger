import cv2
import numpy as np

# center noktasının etrafındaki contour yoğunluğuna göre centerı kaydır


class Gate():

    # constans

    lowerh_gate = 24
    lowers_gate = 89
    lowerv_gate = 0
    upperh_gate = 73
    uppers_gate = 145
    upperv_gate = 255

    """
    # Üst kapıdan geçiyor
    lowerh_gate = 42
    lowers_gate = 100
    lowerv_gate = 59
    upperh_gate = 76
    uppers_gate = 254
    upperv_gate = 133
    """

    lower_color_gate = np.array([lowerh_gate, lowers_gate, lowerv_gate])
    upper_color_gate = np.array([upperh_gate, uppers_gate, upperv_gate])

    border = 45000

    def yaw_right(self, image):
        cv2.putText(image, "Yaw Right", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    def yaw_left(self, image):
        cv2.putText(image, "Yaw Left", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    def ascend(self, image):
        cv2.putText(image, "Go Up", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    def descend(self, image):
        cv2.putText(image, "Go Down", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    def rotate(self, image):
        cv2.putText(image, "Rotate", (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    def get_frame(self, video):
        cap = cv2.VideoCapture(video)
        return cap

    def gate_task(self, cap):
        if cap is None:
            print("Error")
        else:
            max_area = 0
            while True:
                ret, frame = cap.read()

                if ret:
                    # center of frame
                    center_y = int(frame.shape[0] / 2)
                    center_x = int(frame.shape[1] / 2)
                    # line constants
                    x_blank = 120
                    y_blank = 80
                    color = (255, 255, 0)
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
                    mask = cv2.inRange(frame_hsv, self.lower_color_gate, self.upper_color_gate)
                    blur = cv2.GaussianBlur(mask, (5, 5), 0)
                    dilate = cv2.dilate(blur, None, iterations=1)

                    contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if len(contours) > 0:
                        counter = 0
                        sum_cX = 0
                        sum_cY = 0
                        area_sum = 0
                        for cnt in contours:
                            M = cv2.moments(cnt)
                            area = cv2.contourArea(cnt)
                            if area > max_area:
                                max_area = area
                            if M["m00"] != 0:
                                cX = int(M["m10"] / M["m00"])
                                cY = int(M["m01"] / M["m00"])
                                sum_cX += area * cX
                                sum_cY += area * cY
                                area_sum += area
                                cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 1)

                        final_cX = int(sum_cX / area_sum)
                        final_cY = int(sum_cY / area_sum)

                        cv2.circle(frame, (final_cX, final_cY), 7, (255, 0, 0), -1)
                        cv2.putText(frame, "center", (final_cX - 20, final_cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 255, 0), 2)
                        """for cnt in contours:
                            M = cv2.moments(cnt)
                            if M["m00"] != 0:
                                cX = int(M["m10"] / M["m00"])
                                cY = int(M["m01"] / M["m00"])
                                cv2.rectangle(frame, (final_cX - 60, final_cY - 60), (final_cX + 60, final_cY + 60),
                                              (0, 123, 0), 2)
                                if abs(final_cX - cX) < 60 and abs(final_cY - cY) < 60:
                                    counter += 1
                        cv2.putText(frame, "Counter: " + str(counter), (25,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                        if counter > 2:
                            self.rotate(frame)"""


                        """if max_area < self.border:
                            self.rotate(frame)"""
                        if final_cX < vert_line_left:
                            self.yaw_left(frame)
                        elif final_cX > vert_line_right:
                            self.yaw_right(frame)
                        if final_cY < horiz_line_top:
                            self.ascend(frame)
                        elif final_cY > horiz_line_bot:
                            self.descend(frame)

                    cv2.putText(frame, (str(len(contours)) + " contours"), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)
                    cv2.putText(frame, ("max area: " + str(max_area)), (25, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)
                    #cv2.imshow("Video", frame)
                else:
                    break
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

iturov = Gate()
cap = iturov.get_frame("videos/gate_video.avi")
iturov.gate_task(cap)
