
def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    for x in range(255):
        for y in range(255):
            screen[x, y, 0] = x
            screen[x, y, 1] = 128
            screen[x, y, 2] = y


    return screen
