import cv2
import numpy


class PingerScanner():

    heading = 0
    def set_heading(self, heading):
        # heading sabitleme
        return heading

    def forward(self, heading):
        pass

    def turn_right(self):
        pass

    def turn_left(self):
        pass

    def main(self, heading, front_conf, front_dist, right_conf, right_dist):
        # ana tarama kodu
        if front_conf > 90 and front_dist > 500:
            self.heading = self.set_heading(heading)
            self.forward(self.heading)
        else:
            if right_conf > 90 and right_dist > 500:
                self.turn_left()
            elif right_conf > 90 and right_dist < 500:
                self.turn_left()