from PIL import Image, ImageDraw


def mandelbrot(c, treshold, Max_iter=80):
    z = 0
    n = 0
    while abs(z) <= treshold and n < Max_iter:
        z = z*z + c
        n += 1
    return n

def main():
    MAX_ITER = 80
    treshold = 2
    # Image size (pixels)
    WIDTH = 600
    HEIGHT = 400

    # Plot window
    RE_START = -2
    RE_END = 1
    IM_START = -1
    IM_END = 1

    palette = []

    im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coordinate to complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))
            # Compute the number of iterations
            m = mandelbrot(c,treshold, MAX_ITER)
            # The color depends on the number of iterations
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            value = 255 if m < MAX_ITER else 0
            # Plot the point
            draw.point([x, y], (hue, saturation, value))

    im.convert('RGB').save('output.png', 'PNG')

