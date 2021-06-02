import pyopencl as cl
from matplotlib import pyplot as plt
import numpy as np

# %pylab inline

# Create context (containing platform and device information) and command queue
ctx = cl.create_some_context()
devices = ctx.get_info(cl.context_info.DEVICES)
print(devices)


def mandelbrot_gpu(input):
    queue = cl.CommandQueue(ctx)
    output = np.zeros(input.shape).astype(np.int32)
    # Source of the kernel itself.
    prg = cl.Program(ctx, """
    __kernel void mandelbrot(
        __global const float2 *input,
        __global int *output)
    {
        int maxiter = 50;
        int gid = get_global_id(0);
        float real = input[gid].x;
        float imag = input[gid].y;
        output[gid] = 0;
        for(int i = 0; i < maxiter; i++) {
            float real2 = real*real, imag2 = imag*imag;
            if (real*real + imag*imag > 2.0f){
                 output[gid] = i;
                 return;
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


def mandelbrot():
    width = 16000
    height = 16000
    xmin, xmax = -2.0, 1.0  # x range
    ymin, ymax = -1.5, 1.5  # y range
    a = np.linspace(xmin, xmax, width).astype(np.float32)
    b = np.linspace(ymin, ymax, height).astype(np.float32)
    x, y = np.meshgrid(a, b)
    z = x + y * 1j
    z = z.flatten()
    o = mandelbrot_gpu(z)
    return (o)


result = mandelbrot()
result = np.reshape(result, (16000, 16000))
plt.imshow(result, cmap=plt.cm.hot)  # plot the image
plt.show()