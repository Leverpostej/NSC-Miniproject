# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 10:44:38 2021

@author: NCJ
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("MandelbrotSet.pyx")
)

