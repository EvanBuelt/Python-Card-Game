__author__ = 'Evan'
import math


class SquareHitbox:
    def __init__(self, x, y, width, height, angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = math.radians(angle)

        self.points = []
        self.rotatedPoints = []

        self._get_points()
        self._get_rotated_points()

    def collide(self, x, y):
        # Assuming points a, b, c, and d, and a point m with coordinates (x, y).
        # Check the vector from point a to point m against the vectors from a to b and a to d.
        # Vector math to check if a point is inside the hitbox.  Allows hitbox to be rotated to any angle
        vector_am = Vector(self.rotatedPoints[0].x - x,
                           self.rotatedPoints[0].y - y)
        vector_ab = Vector(self.rotatedPoints[0].x - self.rotatedPoints[1].x,
                           self.rotatedPoints[0].y - self.rotatedPoints[1].y)
        vector_ad = Vector(self.rotatedPoints[0].x - self.rotatedPoints[3].x,
                           self.rotatedPoints[0].y - self.rotatedPoints[3].y)
        if 0 <= vector_am * vector_ab < vector_ab * vector_ab and 0 <= vector_am * vector_ad < vector_ad * vector_ad:
            return True
        else:
            return False

    def update(self, x=None, y=None, width=None, height=None, angle=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if angle is not None:
            self.angle = math.radians(angle)

        self._get_points()
        self._get_rotated_points()

    def _get_points(self):
        self.points = []
        self.points.append(Point(self.x, self.y))
        self.points.append(Point(self.x + self.width, self.y))
        self.points.append(Point(self.x + self.width, self.y + self.height))
        self.points.append(Point(self.x, self.y + self.height))

    def _get_rotated_points(self):
        # Use Point 0 as reference for rotating every point
        x, y = self.points[0].x, self.points[0].y

        self.rotatedPoints = []
        for point in self.points:
            self.rotatedPoints.append(point.copy())

        for point in self.rotatedPoints:
            point.rotate_counterclockwise(x, y, self.angle)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate_clockwise(self, angle_radians, x=0, y=0):
        # Rotate about the point (x, y) clockwise by a given angle in radians
        nx = math.cos(angle_radians) * (self.x - x) - math.sin(angle_radians) * (self.y - y) + x
        ny = math.sin(angle_radians) * (self.x - x) + math.cos(angle_radians) * (self.y - y) + y

        self.x = nx
        self.y = ny

    def rotate_counterclockwise(self, x, y, angle_radians):
        # Rotate about the point (x, y) counter clockwise by a given angle in radians
        self.rotate_clockwise(x, y, -1 * angle_radians)

    def scale(self, x, y, scalar):
        # Scales about the point (x, y) by a constant scalar
        self.x = math.fabs(self.x - x) * scalar + x
        self.y = math.fabs(self.y - y) * scalar + y

    def reflect(self, axis):
        if axis is 'x' or axis is 'X':
            self.x *= -1
        elif axis is 'y' or axis is 'Y':
            self.y *= -1


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def get_radians(self):
        return math.acos(self.x / self.get_magnitude())

    def get_degrees(self):
        return math.degrees(self.get_radians())

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, num):
        self.x *= num
        self.y *= num

    def __idiv__(self, num):
        self.x /= num
        self.y /= num

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
