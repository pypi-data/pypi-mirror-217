import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

setup(
    packages=find_packages(),
    install_requires=["cffi>=1.15.0"],
    setup_requires=["cffi>=1.15.0"],
    cffi_modules=[
        "./cephes4py/build_hcephes.py:ffibuilder",
    ],
    include_package_data=True,
    package_data={'': ['interface.h']},
)