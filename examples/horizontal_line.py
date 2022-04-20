def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    y = 200

    for x in range(200):
        screen[x, y, 0] = 255

    return screen
