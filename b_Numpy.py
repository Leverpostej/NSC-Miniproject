import numpy as np
import matplotlib.pyplot as plt
import h5py
import time


def mandelbrot_set(c, threshold, num_iterations):
    # determine for each point c of a part of the complex plane, whether z_n is bounded

    # complex number, real part represented by a displacement along the x-axis
    # imaginary part by a displacement along the y-axis
    z = 0
    for g in range(num_iterations):
        z = z ** 2 + c
    n = np.abs(z) < threshold
    return n, z


def main():
    num_iterations = 80
    threshold = 2
    start = time.time()
    x, y = np.ogrid[-2:1:5000j, -1.5:1.5:5000j]
    c = x + 1j * y
    n, z = mandelbrot_set(c, threshold, num_iterations)
    print("computation time", time.time()-start)
    plt.imshow(n.T, extent=[-2, 1, -1.5, 1.5], cmap=plt.cm.get_cmap("hot"), aspect='auto')

    # plt.show()
    plt.savefig('numpy.png')
    h5f = h5py.File('numpy.h5', 'w')
    h5f.create_dataset('dataset_1', data=z)
    h5f.close()


main()
