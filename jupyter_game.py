import async_jupyter as asj
import PIL.Image
import asyncio
import numpy as np

import PIL.Image
from io import BytesIO

import IPython
import ipywidgets as widgets


def png_bytes(array):
    a = np.uint8(np.transpose(array, [1,0,2]))
    f = BytesIO()
    PIL.Image.fromarray(a).save(f, 'png')

    return f.getvalue()

def to_ipython_image(a):

    return widgets.Image(value=png_bytes(a),
    format='png', width=a.shape[0], height=a.shape[1])


def run(loop, screen_size):

    event_loop = asj.get_event_loop()
    screen_shape = screen_size + [3]

    ipython_image = to_ipython_image(np.zeros(screen_shape, dtype=np.uint8))

    # IPython.display.Image(data=f.getvalue(), width=a.shape[1] * 4, height=a.shape[0] * 4)


    IPython.display.display(ipython_image)

    async def render_loop():
        while True:
            screen = np.zeros(screen_shape, dtype=np.uint8)
    
            updated_screen = loop(0, screen, 0, 0, False, False, False)  

            ipython_image.value = png_bytes(updated_screen)

            print('.')

            await asyncio.sleep(1)


    event_loop.create_task(render_loop())
        
    