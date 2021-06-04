import time as time
import dask.array as da
from dask.distributed import Client, wait
import h5py


def mandelbrot_set(c, threshold, num_iterations):
    # determine for each point c of a part of the complex plane, whether z_n is bounded
    # complex number, real part represented by a displacement along the x-axis,
    # imaginary part by a displacement along the y-axis

    z = 0
    for g in range(num_iterations):
        z = z ** 2 + c
    n = da.absolute(z) < threshold
    return n, z


def dask_mandelbrot():
    client = Client('10.92.0.148:8786')
    print(client)

    num_iterations = 80
    threshold = 2
    chunk_shape = (5000,)
    x = da.linspace(-2, 1, 5000, chunks=chunk_shape)
    y = da.linspace(-1.5, 1.5, 5000, chunks=chunk_shape)
    
    x, y = da.meshgrid(x, y)

    c = x + 1j*y

    counts = client.submit(mandelbrot_set, c, threshold, num_iterations, pure=False)

    wait(counts)

    n, z = counts.result()  

    return n, z


def main():
    start_time = time.time()
    n, z = dask_mandelbrot()

    # plt.imsave("Try.jpg", n, cmap=plt.cm.hot)  # plot the image

    stop_time = time.time()

    print(stop_time - start_time)

    h5f = h5py.File('dask.h5', 'w')
    h5f.create_dataset('dataset_1', data=z)
    h5f.close()

    # plt.imshow(n.T,extent=[-2,1,-1.5,1.5],cmap=plt.cm.get_cmap("hot"), aspect='auto')

    # plt.show()


if __name__ == "__main__":
    main()
