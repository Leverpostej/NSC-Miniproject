import pyopencl as cl
from matplotlib import pyplot as plt
import numpy as np
import h5py
import time


def mandelbrot_gpu(input, ctx):
    queue = cl.CommandQueue(ctx)
    output = np.zeros(input.shape).astype(np.int32)
    # Source of the kernel itself.
    prg = cl.Program(ctx, """
    __kernel void mandelbrot(
        __global const float2 *input,
        __global int *output)
    {
        int maxiter = 80;
        int gid = get_global_id(0);
        float real = input[gid].x;
        float imag = input[gid].y;
        output[gid] = 0;
        for(int i = 0; i < maxiter; i++) {
            float real2 = real*real, imag2 = imag*imag;
            if (real*real + imag*imag > 2.0f){
                 output[gid] = i;
            }
            imag = 2* real*imag + input[gid].y;
            real = real2 - imag2 + input[gid].x;
        }
    }
    """).build()

    mf = cl.mem_flags
    input_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                             hostbuf=input)
    output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output.nbytes)

    Event = prg.mandelbrot(queue, output.shape, None, input_opencl,
                           output_opencl)
    Event.wait()
    cl.enqueue_copy(queue, output, output_opencl)

    return output


def mandelbrot(ctx):
    width = 5000
    height = 5000
    x_min, x_max = -2.0, 1.0  # x range
    y_min, y_max = -1.5, 1.5  # y range
    a = np.linspace(x_min, x_max, width).astype(np.float32)
    b = np.linspace(y_min, y_max, height).astype(np.float32)
    x, y = np.meshgrid(a, b)
    z = x + y * 1j
    z = z.flatten()
    o = mandelbrot_gpu(z, ctx)
    return o, z


def main():
    # Create context (containing platform and device information) and command queue
    ctx = cl.create_some_context()
    devices = ctx.get_info(cl.context_info.DEVICES)
    print(devices)
    start = time.time()
    result, z = mandelbrot(ctx)
    print("computation time", time.time()-start)
    result = np.reshape(result, (5000, 5000))
    plt.imshow(result, cmap=plt.cm.hot)  # plot the image
    # plt.show()
    plt.savefig('gpu.png')
    h5f = h5py.File('gpu.h5', 'w')
    h5f.create_dataset('dataset_1', data=z)
    h5f.close()


main()
