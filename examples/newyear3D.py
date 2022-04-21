import random

class Particle:
    def __init__(self, x, y, z, v_x, v_y, v_z, color):
        self.x = x
        self.y = y
        self.z = z

        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

        self.color = color

    def update(self, screen):

        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z

        self.draw(screen)

    def draw(self, screen):
        projected_x = 320 + 320 * (self.x / self.z)
        projected_y = 240 + 240 * (self.y / self.z)

        if projected_x < 0:
            return

        if projected_y < 0:
            return

        if projected_x >= 640:
            return

        if projected_y >= 480:
            return

        for i in range(3):
            projected_color = self.color[i] * (160 - self.z) / 160

            screen[int(projected_x), int(projected_y), i] = int(projected_color)


def clear_screen(screen):
    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0


class Firework:
    def __init__(self, x, y, z):
        self.particles = []

        for i in range(100):
            self.particles.append(Particle(x, y, z,
                                           random.random() * 2 - 1, random.random() * 2 - 1, random.random() * 2 - 1,
                                           [255, 200, 0]))

    def update(self, screen):
        for particle in self.particles:
            particle.v_y -= .01
            particle.update(screen)


fireworks = [Firework(random.random() * 640 - 320, random.random() * 480 - 240, 120 + random.random() * 40) for i in range(20)]


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global fireworks
    clear_screen(screen)

    [firework.update(screen) for firework in fireworks]

    return screen


