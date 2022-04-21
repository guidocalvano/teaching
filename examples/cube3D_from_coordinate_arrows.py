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

    def add(self, other):
        total = Arrow3D(0, 0, 0)

        total.x = self.x + other.x
        total.y = self.y + other.y
        total.z = self.z + other.z

        return total

    def scale(self, s):
        return Arrow3D(self.x * s, self.y * s, self.z * s)

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

def line_cube(screen, position, to_right, to_top, to_back):


    left_bottom_front = position.add(to_right.scale(-1)).add(to_top.scale(-1)).add(to_back.scale(-1)).project_on_screen()

    left_bottom_back = position.add(to_right.scale(-1)).add(to_top.scale(-1)).add(to_back.scale(1)).project_on_screen()
    left_top_front = position.add(to_right.scale(-1)).add(to_top.scale(1)).add(to_back.scale(-1)).project_on_screen()
    right_bottom_front = position.add(to_right.scale(1)).add(to_top.scale(-1)).add(to_back.scale(-1)).project_on_screen()

    left_top_back = position.add(to_right.scale(-1)).add(to_top.scale(1)).add(to_back.scale(1)).project_on_screen()
    right_bottom_back = position.add(to_right.scale(1)).add(to_top.scale(-1)).add(to_back.scale(1)).project_on_screen()
    right_top_front = position.add(to_right.scale(1)).add(to_top.scale(1)).add(to_back.scale(-1)).project_on_screen()

    right_top_back = position.add(to_right.scale(1)).add(to_top.scale(1)).add(to_back.scale(1)).project_on_screen()

    line(screen, left_top_front, right_top_front, [255, 0, 0])
    line(screen, left_top_front, left_bottom_front, [255, 0, 0])
    line(screen, left_top_front, left_top_back, [255, 0, 0])
    line(screen, right_top_front, right_top_back, [255, 0, 0])

    line(screen, right_top_front, right_bottom_front, [255, 0, 0])
    line(screen, left_bottom_front, left_bottom_back, [255, 0, 0])

    line(screen, left_bottom_front, right_bottom_front, [255, 0, 0])
    line(screen, right_bottom_front, right_bottom_back, [255, 0, 0])

    line(screen, left_top_back, right_top_back, [255, 0, 0])
    line(screen, left_top_back, left_bottom_back, [255, 0, 0])
    line(screen, right_bottom_back, right_top_back, [255, 0, 0])
    line(screen, left_bottom_back, right_bottom_back, [255, 0, 0])


def clear_screen(screen):
    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0


v = 0
def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global v
    v += .2

    clear_screen(screen)
    line_cube(screen, Arrow3D(0, 0, 50), Arrow3D(20 , 0, 0), Arrow3D(0, 20, 0), Arrow3D(0, 0, 20))

    return screen


