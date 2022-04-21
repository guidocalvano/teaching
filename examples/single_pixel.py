def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    x = 320
    y = 240

    screen[x, y, 0] = 255
    screen[x, y, 1] = 240
    screen[x, y, 2] = 180

    return screen

