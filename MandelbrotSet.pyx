# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 10:55:19 2021

@author: NCJ
"""

import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from mandelbrot import mandelbrot, MAX_ITER

# with numpy
def mandelbrot_set(c, treshold, num_iterations):
    #determine for each point c of a part of the complex plane, whether z_n is bounded



    z = 0 # complex number, real part represented by a displacement along the x-axis, imaginary part by a displacement along the y-axis

    for g in range(num_iterations):
        z = z ** 2 + c
    n = abs(z) < treshold
    return n


num_iterations=16
threshold = 2

x,y=np.ogrid[-2:1:5000j,-1.5:1.5:5000j]
c=x + 1j*y
n = mandelbrot_set(c, threshold, num_iterations)

plt.imshow(n.T,extent=[-2,1,-1.5,1.5],cmap=plt.cm.get_cmap("hot"), aspect='auto')

plt.show()
