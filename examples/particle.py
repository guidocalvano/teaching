
class Particle:

    def __init__(self, x, y, v_x, v_y, color):
        self.x = x
        self.y = y

        self.v_x = v_x
        self.v_y = v_y

        self.color = color

    def update(self, screen):

        self.x += self.v_x
        self.y += self.v_y

        self.draw(screen)

    def draw(self, screen):

        for i in range(3):
            screen[int(self.x), int(self.y), i] = self.color[i]


def clear_screen(screen):
    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0


p = Particle(0, 0, .5, .5, [255, 0, 0])


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global p
    clear_screen(screen)

    p.update(screen)

    return screen


