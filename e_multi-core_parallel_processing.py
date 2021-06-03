import h5py
from numpy import linspace, reshape
from matplotlib import pyplot
from multiprocessing import Pool
import time


def mandelbrot(z):  # computation for one pixel
    c = z
    for n in range(80):
        if abs(z) > 2:
            return n  # divergence test
        z = z * z + c
    return 80


def main(processes):
    x_min, x_max = -2.0, 1  # x range
    y_min, y_max = -1.5, 1.5  # y range
    nx, ny = 5000, 5000  # resolution
    start = time.time()

    X = linspace(x_min, x_max, nx)  # lists of x and y
    Y = linspace(y_min, y_max, ny)  # pixel co-ordinates

    p = Pool(processes=processes)
    z = [complex(x, y) for y in Y for x in X]
    n = p.map(mandelbrot, z)
    print("computation time", time.time()-start)

    n = reshape(n, (nx, ny))  # change to rectangular array

    pyplot.imshow(n)  # plot the image
    # pyplot.show()
    pyplot.savefig('parallel.png')
    h5f = h5py.File('parallel.h5', 'w')
    h5f.create_dataset('dataset_1', data=z)
    h5f.close()


if __name__ == '__main__':
    workers = 8
    main(workers)
