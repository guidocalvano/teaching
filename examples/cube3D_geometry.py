import math


class Arrow2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other_arrow):
        third_arrow = Arrow2D(0, 0)

        third_arrow.x = self.x + other_arrow.x
        third_arrow.y = self.y + other_arrow.y

        return third_arrow

    def scale(self, s):

        scaled_arrow = Arrow2D(self.x * s, self.y * s)

        return scaled_arrow

    def length(self):
        # ac^2 = ab^2 + bc^2
        # ac = sqrt(ab^2 + bc^2)
        # x = bc
        # y = ab
        # l = ac
        l = math.sqrt(self.x * self.x + self.y * self.y)

        return l


class Arrow3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def project_on_screen(self):
        screen_x = self.x / self.z
        screen_y = self.y / self.z

        return Arrow2D(screen_x * 240 + 320, screen_y * 240 + 240)

    def length(self):
        #@TODO explain why this works

        l = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

        return l

    def add(self, other):
        total = Arrow3D(0, 0, 0)

        total.x = self.x + other.x
        total.y = self.y + other.y
        total.z = self.z + other.z

        return total

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.add(-other)

    def scale(self, s):
        return Arrow3D(self.x * s, self.y * s, self.z * s)

    def __mul__(self, s):
        return self.scale(s)

    def __rmul__(self, s):
        return self.scale(s)

    def __neg__(self):
        return Arrow3D(-self.x, -self.y, -self.z)

class CoordinateSystem:

    def __init__(self, position, x_axis, y_axis, z_axis):
        self.position = position
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis

    def transform(self, arrow):
        return self.position + self.x_axis * arrow.x + self.y_axis * arrow.y + self.z_axis * arrow.z

class Geometry:

    def __init__(self, points, lines):
        self.points = points
        self.lines = lines

    @staticmethod
    def cube():
        right = Arrow3D(1, 0, 0)
        top   = Arrow3D(0, 1, 0)
        back  = Arrow3D(0, 0, 1)

        points = []
        lines = []

        for x in [-right, right]:
            for y in [-top, top]:
                for z in [-back, back]:
                    points.append(x + y + z)

        for first in range(len(points)):
            for second in range(first + 1, len(points)):
                if (points[first] - points[second]).length() == 2:
                    lines.append([first, second])

        return Geometry(points, lines)

    def outside_coordinate_system(self, coordinate_system):
        transformed_points = []

        for point in self.points:
            transformed_points.append(coordinate_system.transform(point))

        return Geometry(transformed_points, self.lines.copy())

    def draw(self, screen, color):
        for l in self.lines:
            start = self.points[l[0]]
            finish = self.points[l[1]]

            line(screen, start.project_on_screen(), finish.project_on_screen(), color)

def line(screen, start, finish, color):
    from_start_to_finish = finish.add(start.scale(-1))

    number_of_steps = int(from_start_to_finish.length())

    step_arrow = from_start_to_finish.scale(1/number_of_steps)

    for i in range(number_of_steps):
        next_step = start.add(step_arrow.scale(i))

        screen_x = int(next_step.x)
        screen_y = int(next_step.y)

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
    position = Arrow3D(0, 0, 50)
    x_axis = Arrow3D(20 * math.cos(angle), 0, 20 * math.sin(angle))
    y_axis = Arrow3D(0, 20, 0)
    z_axis = Arrow3D(20 * math.cos(angle + .5 * math.pi), 0, 20 * math.sin(angle + .5 * math.pi))

    coordinate_system = CoordinateSystem(position, x_axis, y_axis, z_axis)
    cube = Geometry.cube()

    transformed_cube = cube.outside_coordinate_system(coordinate_system)

    transformed_cube.draw(screen, [0, 0, 255])
    return screen

