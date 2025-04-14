import math
import numpy as np


def project_on_screen(arrow3D):
    arrow2D = arrow3D[[0, 1]]
    return 240 * arrow2D / arrow3D[2] + [320, 240]


def length(arrow):
    return np.linalg.norm(arrow)


class CoordinateSystem:

    def __init__(self, position, x_axis, y_axis, z_axis):
        self.position = position
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis

    def transform(self, arrow):
        return self.position + self.x_axis * arrow[0] + self.y_axis * arrow[1] + self.z_axis * arrow[2]


class Geometry:

    def __init__(self, points, lines, surfaces):
        self.points = points
        self.lines = lines
        self.surfaces = surfaces

    @staticmethod
    def cube():
        right = np.array([1., 0, 0])
        top = np.array([0, 1., 0])
        back = np.array([0, 0, 1.])

        points = []
        lines = []

        for x in [-right, right]:
            for y in [-top, top]:
                for z in [-back, back]:
                    points.append(x + y + z)

        for first in range(len(points)):
            for second in range(first + 1, len(points)):
                if length(points[first] - points[second]) == 2:
                    lines.append([first, second])

        return Geometry(np.array(points), np.array(lines))

    @staticmethod
    def tetraeder():
        a = np.array([0., 0., 0.])
        b = np.array([1., 0., 0.])
        #@TODO explain how we make the tetraeder using pythagoras a = sqrt(c*c - b*b)

        # middle_a_b = a + (b - a) / 2
        # middle_a_b = a + (b - a) * .5
        # middle_a_b = a + .5 * b - .5 * a
        # middle_a_b = a - .5 * a + .5 * a
        middle_a_b = .5 * a + .5 * b

        #@TODO explain hadamard product
        middle_a_b_squared = middle_a_b * middle_a_b

        distance_c = np.sqrt(1. * 1. - np.sum(middle_a_b_squared))

        c = middle_a_b + np.array([0., 0., distance_c])

        middle_a_b_c = (a + b + c) / 3.

        middle_a_b_c_squared = middle_a_b_c * middle_a_b_c

        height_d = np.sqrt(1. * 1. - np.sum(middle_a_b_c_squared))

        d = middle_a_b_c + np.array([0., height_d, 0.])

        points = np.array([a, b, c, d])

        center = np.sum(points, axis=0) / 4.

        centered_points = []

        for p in points:
            centered_points.append(p - center)

        lines = []
        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                lines.append([i, j])

        surfaces = []
        for i in range(len(points) - 2):
            for j in range(i + 1, len(points) - 1):
                for k in range(j + 1, len(points)):

                    surfaces.append([i, j, k])

        return Geometry(np.array(centered_points), np.array(lines), np.array(surfaces))

    def outside_coordinate_system(self, coordinate_system):
        transformed_points = []

        for point in self.points:
            transformed_points.append(coordinate_system.transform(point))

        return Geometry(np.array(transformed_points), self.lines.copy(), self.surfaces.copy())

    def draw(self, screen, color):
        for l in self.lines:
            start = project_on_screen(self.points[l[0]])
            finish = project_on_screen(self.points[l[1]])

            line(screen, start, finish, color)

        for s in self.surfaces:
            a = project_on_screen(self.points[s[0]])
            b = project_on_screen(self.points[s[1]])
            c = project_on_screen(self.points[s[2]])

            triangle_filled(screen, a, b, c, color)


def line(screen, start, finish, color):
    from_start_to_finish = finish - start

    number_of_steps = int(length(from_start_to_finish)) + 1

    step_arrow = from_start_to_finish * 1. / number_of_steps

    for i in range(number_of_steps):
        next_step = start + i * step_arrow

        screen_x = int(next_step[0])
        screen_y = int(next_step[1])

        if screen_x < 0:
            continue

        if screen_x >= 640:
            continue

        if screen_y < 0:
            continue

        if screen_y >= 480:
            continue

        for c in range(len(color)):
            screen[screen_x, screen_y, c] = color[c]

def triangle_filled(screen, a, b, c, color):
    triangle_origin = a
    triangle_x_axis, x_count = unit_axis(triangle_origin, b)
    triangle_y_axis, y_count = unit_axis(triangle_origin, c)

    for x in range(int(x_count)):
        for y in range(int(y_count)):
            if x / x_count + y / y_count > 1.:
                continue

            point = triangle_origin + x * triangle_x_axis + y * triangle_y_axis
            screen[int(point[0]), int(point[1]), :] = color



def unit_axis(origin, point):
    origin_to_point = point - origin
    distance = length(origin_to_point)

    unit_axis = origin_to_point / distance

    return unit_axis, distance

def clear_screen(screen):
    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0


angle = 0


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global angle
    angle += .2

    while angle > math.pi * 2:
        angle -= math.pi * 2

    clear_screen(screen)
    position = np.array([0, 0, 50])
    x_axis = np.array([20 * math.cos(angle), 0, 20 * math.sin(angle)])
    y_axis = np.array([0, 20, 0])
    z_axis = np.array([20 * math.cos(angle + .5 * math.pi), 0, 20 * math.sin(angle + .5 * math.pi)])

    coordinate_system = CoordinateSystem(position, x_axis, y_axis, z_axis)
    cube = Geometry.tetraeder()

    transformed_cube = cube.outside_coordinate_system(coordinate_system)

    transformed_cube.draw(screen, [0, 0, 255])

    return screen

