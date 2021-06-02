from PIL import Image, ImageDraw
import h5py
import time


def mandelbrot(c, threshold, max_iter=80):
    z = 0
    n = 0
    while abs(z) <= threshold and n < max_iter:
        z = z*z + c
        n += 1
    return n, z


def main():
    max_iter = 80
    threshold = 2
    # Image size (pixels)
    width = 600
    height = 400

    # Plot window
    re_start = -2
    re_end = 1
    im_start = -1
    im_end = 1

    im = Image.new('HSV', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    start = time.time()
    z = []
    for x in range(0, width):
        for y in range(0, height):
            # Convert pixel coordinate to complex number
            c = complex(re_start + (x / width) * (re_end - re_start),
                        im_start + (y / height) * (im_end - im_start))
            # Compute the number of iterations
            m, z2 = mandelbrot(c, threshold, max_iter)
            # The color depends on the number of iterations
            hue = int(255 * m / max_iter)
            saturation = 255
            value = 255 if m < max_iter else 0
            # Plot the point
            draw.point([x, y], (hue, saturation, value))
            z.append(z2)
    h5f = h5py.File('naive.h5', 'w')
    h5f.create_dataset('dataset_1', data=z)
    h5f.close()
    print("computation time", time.time()-start)
    im.convert('RGB').save('output.png', 'PNG')


main()
