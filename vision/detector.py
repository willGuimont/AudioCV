import cv2
import numpy as np


class Detector:

    __slider_window_name = "HSV range"

    __min_h_slider_name = "Min Hue"
    __max_h_slider_name = "Max Hue"

    __min_s_slider_name = "Min Saturation"
    __max_s_slider_name = "Max Saturation"

    __min_v_slider_name = "Min Value"
    __max_v_slider_name = "Max Value"

    __structure_elem_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    __kernel = np.ones((5, 5), np.uint8)

    __min_area_contour = 100

    def __init__(self):
        """
        Create a detector object
        """
        # Init sliders
        cv2.namedWindow(Detector.__slider_window_name)

        cv2.createTrackbar(Detector.__min_h_slider_name, Detector.__slider_window_name, 0, 151, self.__nothing)
        cv2.createTrackbar(Detector.__max_h_slider_name, Detector.__slider_window_name, 0, 151, self.__nothing)

        cv2.createTrackbar(Detector.__min_s_slider_name, Detector.__slider_window_name, 0, 256, self.__nothing)
        cv2.createTrackbar(Detector.__max_s_slider_name, Detector.__slider_window_name, 0, 256, self.__nothing)

        cv2.createTrackbar(Detector.__min_v_slider_name, Detector.__slider_window_name, 0, 256, self.__nothing)
        cv2.createTrackbar(Detector.__max_v_slider_name, Detector.__slider_window_name, 0, 256, self.__nothing)

        # Defaults value determined by experience
        cv2.setTrackbarPos(Detector.__min_h_slider_name, Detector.__slider_window_name, 95)
        cv2.setTrackbarPos(Detector.__max_h_slider_name, Detector.__slider_window_name, 139)

        cv2.setTrackbarPos(Detector.__min_s_slider_name, Detector.__slider_window_name, 39)
        cv2.setTrackbarPos(Detector.__max_s_slider_name, Detector.__slider_window_name, 256)

        cv2.setTrackbarPos(Detector.__min_v_slider_name, Detector.__slider_window_name, 89)
        cv2.setTrackbarPos(Detector.__max_v_slider_name, Detector.__slider_window_name, 256)

    # Empty callback for the sliders
    @staticmethod
    def __nothing(var):
        """
        Does nothing
        :param var: value of the slider (not used)
        :return: None
        """
        pass

    @staticmethod
    def __cost_contour(cnt):
        """
        Compute the cost on cnt
        :param cnt: Contour
        :return: Cost
        """
        area = cv2.contourArea(cnt)

        # Discard contour too small
        if area < Detector.__min_area_contour:
            return -1

        try:
            cost = 1 / area  # must be close to 0 # so that area /(perimeter * radius) = 1
            return cost
        except ZeroDivisionError:
            return -1

    def __get_sorted_contour(self, contours):
        """
        Return the contour with the lower cost
        :param contours: List of contours
        :return: Best contour
        """
        contour_array = []
        for cnt in contours:
            cost = self.__cost_contour(cnt)
            if cost != -1:
                contour_array.append([cnt, cost])
        contour_array.sort(key=lambda x: x[1])  # Sort by cost
        cnts = [x[0] for x in contour_array]  # Get only cnts
        return cnts

    # Path may be a video file path or an integer for live cam
    def detect(self, frame, num_of_objects=1):
        """
        Find the ball
        :param frame: Frame
        :return: Position, Drawn image, threshold
        """

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        draw = frame.copy()

        min_h = cv2.getTrackbarPos(Detector.__min_h_slider_name, Detector.__slider_window_name)
        min_s = cv2.getTrackbarPos(Detector.__min_s_slider_name, Detector.__slider_window_name)
        min_v = cv2.getTrackbarPos(Detector.__min_v_slider_name, Detector.__slider_window_name)

        max_h = cv2.getTrackbarPos(Detector.__max_h_slider_name, Detector.__slider_window_name)
        max_s = cv2.getTrackbarPos(Detector.__max_s_slider_name, Detector.__slider_window_name)
        max_v = cv2.getTrackbarPos(Detector.__max_v_slider_name, Detector.__slider_window_name)

        in_range = cv2.inRange(hsv, (min_h, min_s, min_v), (max_h, max_s, max_v))
        # in_range = cv2.morphologyEx(in_range, cv2.MORPH_CLOSE, Detector.__structure_elem_ellipse) # kernel?
        in_range = cv2.dilate(in_range, Detector.__kernel, iterations=1)
        in_range = cv2.erode(in_range, Detector.__kernel, iterations=3)

        im2, contours, hierarchy = cv2.findContours(in_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sorted_contour = self.__get_sorted_contour(contours)
        selected_contours = sorted_contour[:num_of_objects]
        selected_moments = [cv2.moments(x) for x in selected_contours]

        positions = [[int(M['m10']/M['m00']), int(M['m01']/M['m00'])] for M in selected_moments]

        for cnt in selected_contours:
            if len(cnt) >= 5:  # Min 5 points to fit ellipse
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(draw, ellipse, (0, 255, 0), 2)
            else:
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(draw, center, radius, (0, 255, 0), 2)

        if len(sorted_contour) == 0:
            return positions, draw, in_range

        return positions, draw, in_range
