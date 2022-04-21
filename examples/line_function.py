import math

class Arrow:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other_arrow):
        third_arrow = Arrow(0, 0)

        third_arrow.x = self.x + other_arrow.x
        third_arrow.y = self.y + other_arrow.y

        return third_arrow

    def scale(self, s):

        scaled_arrow = Arrow(self.x * s, self.y * s)

        return scaled_arrow

    def length(self):
        # ac^2 = ab^2 + bc^2
        # ac = sqrt(ab^2 + bc^2)
        # x = bc
        # y = ab
        # l = ac
        l = math.sqrt(self.x * self.x + self.y * self.y)

        return l

def line(screen, start, finish, color):
    from_start_to_finish = finish.add(start.scale(-1))

    number_of_steps = int(from_start_to_finish.length())

    step_arrow = from_start_to_finish.scale(1/number_of_steps)

    for i in range(number_of_steps):
        next_step = start.add(step_arrow.scale(i))

        screen_x = int(next_step.x)
        screen_y = int(next_step.y)

        for c in range(len(color)):
            screen[screen_x, screen_y, c] = color[c]

def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    line(screen, Arrow(20, 20), Arrow(10, 40), [240, 0, 240])

    return screen

