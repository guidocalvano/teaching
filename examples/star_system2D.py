import random
import numpy as np

class Star:
    def __init__(self, x, y, v_x, v_y, mass):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.f_x = 0.0
        self.f_y = 0.0

        self.mass = mass

    def update(self, screen):
        self.v_x += self.f_x
        self.x += self.v_x

        self.v_y += self.f_y
        self.y += self.v_y

        self.f_x = 0.0
        self.f_y = 0.0

        self.draw(screen)

    def gravity_interaction(self, p):
        d_p = self.distance(p)
        G = 100.0  # the gravity constant
        gravity_force = G * p.mass * self.mass / (d_p * d_p)

        dx = p.x - self.x
        dy = p.y - self.y

        df_x = gravity_force * dx / d_p
        df_y = gravity_force * dy / d_p

        self.f_x += df_x
        self.f_y += df_y

        p.f_x -= df_x
        p.f_y -= df_y

    def distance(self, p):
        dx = p.x - self.x
        dy = p.y - self.y

        return np.sqrt(dx * dx + dy * dy)

    def draw(self, screen):
        if not self.is_on_screen(screen):
            return

        for i in range(3):
            screen[int(self.x), int(self.y), i] = 255

    def is_on_screen(self, screen):
        if self.x >= screen.shape[0]:
            return False

        if self.y >= screen.shape[1]:
            return False

        if self.x < 0:
            return False

        if self.y < 0:
            return False

        return True

def clear_screen(screen):
    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0

star_count = 30
stars = []

for i in range(star_count):

    x = random.random() * 640
    y = random.random() * 320

    v_x = random.random() * 2 - 1
    v_y = random.random() * 2 - 1

    mass = random.random()

    stars.append(Star(x, y, v_x, v_y, mass))


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    clear_screen(screen)

    for i in range(len(stars) - 1):
        for j in range(i + 1, len(stars)):
            stars[i].gravity_interaction(stars[j])

    for star in stars:
        star.update(screen)

    return screen
