def loop(elapsed_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up):

    x = 50
    y = 50

    red = 0
    green = 1
    blue = 2

    redness = 255
    greenness = 0
    blueness = 0

    screen[x, y, red] = redness
    screen[x, y, green] = greenness
    screen[x, y, blue] = blueness

    return screen

