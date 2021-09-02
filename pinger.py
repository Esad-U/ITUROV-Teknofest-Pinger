import cv2
import numpy as np


class Pinger():

    # constans
    check = False
    yaw = 0
    altitude = 500
    center_heading = None
    heading_error = 0
    altitude_error = 0
    lowerh = 0
    lowers = 114
    lowerv = 168
    upperh = 59
    uppers = 220
    upperv = 255
    lower_color = np.array([lowerh, lowers, lowerv])
    upper_color = np.array([upperh, uppers, upperv])

    def yaw_right(self, image):
        cv2.putText(image, "Yaw Right", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    def yaw_left(self, image):
        cv2.putText(image, "Yaw Left", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    def ascend(self, image):
        cv2.putText(image, "Go Up", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return 350

    def descend(self, image):
        cv2.putText(image, "Go Down", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return 300

    def get_frame(self, video):
        cap = cv2.VideoCapture(video)
        return cap

    def pinger_task_heading(self, frame, heading):


        # center of frame
        center_y = int(frame.shape[0] / 2)
        center_x = int(frame.shape[1] / 2)
        # line constants
        x_blank = 60
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
        mask = cv2.inRange(frame_hsv, self.lower_color, self.upper_color)
        blur = cv2.GaussianBlur(mask, (5, 5), 0)
        blur = cv2.GaussianBlur(mask, (5, 5), 0)

        contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        if len(contours) > 0:
            sum_cX = 0
            sum_cY = 0
            area_sum = 0
            for cnt in contours:
                M = cv2.moments(cnt)
                area = cv2.contourArea(cnt)
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
            cv2.putText(frame, (str(len(contours)) + " contours"), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

            if not self.check:
                if final_cX < vert_line_left:
                    self.yaw_left(frame)
                    self.yaw = 30
                elif final_cX > vert_line_right:
                    self.yaw_right(frame)
                    self.yaw = 90
                if final_cX > vert_line_left and final_cX < vert_line_right:
                    self.center_heading = heading
                    self.check = True

            if final_cY < horiz_line_top:
                self.ascend(frame)
                self.altitude = 400
            elif final_cY > horiz_line_bot:
                self.descend(frame)
                self.altitude = 320

        return frame

    def pinger_task(self, frame):
        heading_error = 0
        altitude_error = 0
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
        mask = cv2.inRange(frame_hsv, self.lower_color, self.upper_color)
        blur = cv2.GaussianBlur(mask, (5, 5), 0)
        blur = cv2.GaussianBlur(mask, (5, 5), 0)

        contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        if len(contours) > 0:
            sum_cX = 0
            sum_cY = 0
            area_sum = 0
            for cnt in contours:
                M = cv2.moments(cnt)
                area = cv2.contourArea(cnt)
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
            cv2.putText(frame, "center", (final_cX - 20, final_cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            heading_error = 320 - final_cX

            altitude_error = final_cY - 240 + 60

        cv2.putText(frame, (str(len(contours)) + " contours"), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        return frame, heading_error, altitude_error
