import random

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

        if self.x < 0:
            return

        if self.y < 0:
            return

        if self.x >= 640:
            return

        if self.y >= 480:
            return

        for i in range(3):
            screen[int(self.x), int(self.y), i] = self.color[i]


def clear_screen(screen):
    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0


class Firework:
    def __init__(self, x, y):
        self.particles = []

        for i in range(100):
            self.particles.append(Particle(x, y, random.random() * 2 - 1, random.random() * 2 - 1, [255, 0, 0]))

    def update(self, screen):
        for particle in self.particles:
            particle.v_y -= .01
            particle.update(screen)

fireworks = [Firework(random.random() * 640, random.random() * 480) for i in range(6)]

def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global fireworks
    # clear_screen(screen)

    [firework.update(screen) for firework in fireworks]

    return screen


