#!/usr/bin/env python
# -*- encoding: utf8 -*-
import io
import os

from setuptools import setup
from distutils.core import Extension
import numpy


long_description = """
Source code: https://github.com/aaspip/pyseistr-win""".strip() 


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")).read()

setup(
    name="pyseistr-win",
    version="0.0.1",
    license='GNU General Public License, Version 3 (GPLv3)',
    description="A python package for structural denoising and interpolation of multi-channel seismic data",
    long_description=long_description,
    author="pyseistr-win developing team",
    author_email="chenyk2016@gmail.com",
    url="https://github.com/aaspip/pyseistr-win",
    packages=['pyseistrw'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    keywords=[
        "seismology", "earthquake seismology", "exploration seismology", "array seismology", "denoising", "science", "engineering", "structure", "local slope", "filtering"
    ],
    install_requires=[
        "numpy", "scipy", "matplotlib"
    ],
    extras_require={
        "docs": ["sphinx", "ipython", "runipy"]
    }
)
