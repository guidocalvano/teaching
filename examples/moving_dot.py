
x = 0
y = 0

v_x = 1
v_y = 1

red = 255
green = 0
blue = 0


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global x, y, v_x, v_y, red, green, blue

    for i in range(640):
        for j in range(480):
            for color in range(3):
                screen[i, j, color] = 0

    x += v_x
    y += v_y

    screen[x, y, 0] = red
    screen[x, y, 1] = green
    screen[x, y, 2] = blue

    return screen

