
def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    if mouse_is_pressed:
        screen[mouse_x, mouse_y, 0] = 255

    return screen
