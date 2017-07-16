import cv2


class Region:
    def __init__(self, mins, maxs):
        """
        Represent a n-dimension cartesian region of space
        :param mins: List of minimums in all dimensions
        :param maxs: List of maximums in all dimensions
        """
        self.__n = len(mins)
        if self.__n  != len(maxs):
            raise ValueError("Both constraints must be of the same dimension")
        if not all(mins[i] <= maxs[i] for i in range(self.__n)):
            raise ValueError("Mins must be smaller than maxs")
        self.__mins = mins
        self.__maxs = maxs

    def get_dimensions(self):
        """
        Get the number of dimension of the region
        :return: Dimension
        """
        return self.__n

    def draw(self, image, color, thickness=3):
        if self.__n != 2:
            # TODO make it work even for 3D (kinect)
            raise ValueError("Dimension must be 2 to draw on screen")
        cv2.rectangle(image, self.__mins, self.__maxs, color, thickness)

    def is_in_region(self, point):
        """
        Check if the point is inside of the region via the AABB algorithm
        :param point: Point
        :return: Is the point inside of the region
        """
        if self.__n != len(point):
            raise ValueError("Point must be of the same dimension as constraints")
        min_ok = all([point[i] >= self.__mins[i] for i in range(self.__n )])
        max_ok = all([point[i] <= self.__maxs[i] for i in range(self.__n )])

        return min_ok and max_ok

    def get_normalized_relative_pos(self, point):
        """
        Get the normalized relative position of the point inside of the region (0 = min, 1 = max)
        :param point: Point
        :return: List of the normalized position in all dimensions
        """
        dist_min_max = [self.__maxs[i] - self.__mins[i] for i in range()]
        rel_pos = [(point[i] - self.__mins[i]) / dist_min_max[i] for i in range(self.__n)]
        return rel_pos

if __name__ == '__main__':
    region = Region((0, 0, 0), (1, 1, 1))
    print(region.is_in_region((2, 0.5, 0.5)))
