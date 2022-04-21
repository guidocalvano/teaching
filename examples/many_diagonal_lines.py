
x = [10, 20, 30]
y = [40, 30, 20]

v_x = [1, 2, 3]
v_y = [3, 2, 1]

red = 255
green = 0
blue = 0


def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):
    global x, y, v_x, v_y, red, green, blue

    for i in [0, 1, 2]:
        x[i] += v_x[i]
        y[i] += v_y[i]

        if x[i] >= screen.shape[0]:
            x[i] = 0

        if y[i] >= screen.shape[1]:
            y[i] = 0


        screen[x[i], y[i], 0] = red
        screen[x[i], y[i], 1] = green
        screen[x[i], y[i], 2] = blue

    return screen
