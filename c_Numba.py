import numpy as np
from PIL import Image
from numba import jit


PIXEL_SCALE = 200
WIDTH = 3
HEIGHT = 3
XSTART = -2
YSTART = -1.5

image_width = int(PIXEL_SCALE*WIDTH)
image_height = int(PIXEL_SCALE*HEIGHT)

@jit(nopython=True)
def calc(c1, c2):
    x = y = 0
    for i in range(1000):
        x, y = x*x - y*y + c1, 2*x*y + c2
        if x*x + y*y > 4:
            return i+1
    return 0

array = np.zeros((image_height,
                  image_width,
                  3),
                 dtype=np.uint8)

for i in range(image_width):
    c1 = XSTART + i/PIXEL_SCALE
    for j in range(image_height):
        c2 = YSTART + j/PIXEL_SCALE
        v = calc(c1, c2)
        if v:
            array[j, i,] = (255, 255, 255)

img = Image.fromarray(array)
img.save('mandelbrot.png')