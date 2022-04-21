class Arrow:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other_arrow):
        third_arrow = Arrow(0, 0)

        third_arrow.x = self.x + other_arrow.x
        third_arrow.y = self.y + other_arrow.y

        return third_arrow


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    p = Arrow(0, 0)

    v = Arrow(1, 2)

    red = 255
    green = 0
    blue = 0

    for i in range(200):
        p = p.add(v)

        screen_x = int(p.x)
        screen_y = int(p.y)

        screen[screen_x, screen_y, 0] = red
        screen[screen_x, screen_y, 1] = green
        screen[screen_x, screen_y, 2] = blue

    return screen
