import cv2

from math import atan2, pow, sqrt, pi
from regions.region import Region


class RegionPolar(Region):

    def __init__(self, center, mins, maxs):
        """
        Same as regions.region, but warp coordinate in polar form describe easily circulars regions
        A quarter 2D donut shape with an inner radius of 2 and an outer radius of 5 between pi/2 and pi is described as
        mins = [2, pi/2]    (min radius is 2, min angle is pi/2)
        maxs = [5, pi]      (max radius is 5, max angle is pi)
        :param center: Center of the polar region
        :param mins: mins[0] is the radius minimum, mins[1] is the angle minimum
        :param maxs: maxs[0] is the radius maximum, maxs[1] is the angle maximum
        """
        super().__init__(mins, maxs)
        if self.get_dimensions() != 2:
            raise ValueError('Dimension must be 2 to use polar regions, 3D uses RegionSpherical')
        self.__center = center

    def draw(self, image, color, thickness=3):
        cv2.ellipse(image, (int(self.__center[0], int(self.__center[1]))), (self.__mins[0], self.__mins[0]), 0,
                    self.__mins[1], self.__maxs[1], color, thickness)

    def to_polar(self, point):
        """
        Transform a point to polar coordinate around the center of the region
        :param point: Point
        :return: Radius, Angle
        """
        if len(point) != 2:
            raise ValueError('Dimension must be 2 for polar regions')

        x = point[0]
        y = point[1]

        dx = x - self.__center[0]
        dy = y - self.__center[1]

        theta = atan2(dy, dx)
        r = sqrt(pow(dx, 2) + pow(y, 2))

        return r, theta

    def get_normalized_relative_pos(self, point):
        """
        Same as Region.get_normalized_relative_pos(point) but transform the point to polar first
        :param point: Point
        :return: Normalized relative pos
        """
        point = self.to_polar(point)
        return super().get_normalized_relative_pos(point)

    def is_in_region(self, point):
        """
            Same as Region.is_in_region(point) but transform the point to polar first
            :param point: Point
            :return: Is the point inside of the region
        """
        point = self.to_polar(point)
        return super().is_in_region(point)

if __name__ == '__main__':
    region = RegionPolar((0, 0), (0, 0), (1, pi / 2))
    print(region.is_in_region((0.5, 0.5)))
