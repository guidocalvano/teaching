import pyglet
from pyglet.window import mouse
import numpy as np
from pyglet.gl import GLubyte
from loop import loop
import datetime
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def array_to_image_data(a):
    return (GLubyte * a.size)( *np.reshape(np.transpose(a, [1, 0, 2]), [-1] ))

def main():
    window = pyglet.window.Window()
    window.clear()

    screen = np.zeros([window.width, window.height, 3], dtype=np.uint8)

    image_bytes = array_to_image_data(screen)
    pitch = screen.shape[0] * 3
    image = pyglet.image.ImageData(
        screen.shape[0],
        screen.shape[1],
        "RGB",
        image_bytes,
        pitch=pitch
    )

    mouse_x = 0
    mouse_y = 0
    mouse_is_pressed = False
    mouse_went_down = False
    mouse_went_up = False

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        nonlocal last_frame_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up

        if button == mouse.LEFT:
            mouse_is_pressed = True
            mouse_went_down = True

    @window.event
    def on_mouse_motion(x, y, button, modifiers):
        nonlocal last_frame_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up

        mouse_x = x
        mouse_y = y

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        nonlocal last_frame_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up

        mouse_x = x
        mouse_y = y

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        nonlocal last_frame_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up

        if button == mouse.LEFT:
            mouse_is_pressed = False
            mouse_went_up = True


    pyglet.clock.schedule_interval(lambda dt: 0, .00001)
    last_frame_time = datetime.datetime.timestamp(datetime.datetime.now())
    @window.event
    def on_draw():
        nonlocal last_frame_time, screen, mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up

        current_frame_time = datetime.datetime.timestamp(datetime.datetime.now())
        elapsed_time = current_frame_time - last_frame_time
        last_frame_time = current_frame_time
        next_screen = loop(elapsed_time, screen.copy(), mouse_x, mouse_y, mouse_is_pressed, mouse_went_down, mouse_went_up)
        screen[:, :, :] = next_screen[:, :, :]

        image.set_data('RGB', pitch, array_to_image_data(screen))
        image.blit(0,0)

        mouse_went_up = False
        mouse_went_down = False

    pyglet.app.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
