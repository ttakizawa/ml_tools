from glob import glob
from os.path import basename
from os.path import splitext

import setuptools
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ml-tools",
    version="0.0.1",
    author="ttakizawa",
    author_email="zawa78@gmail.com",
    description="It's pip... with git.",
    long_description=long_description,
    url="https://github.com/ttakizawa/ml_tools",
    install_requires=_requires_from_file('requirements.txt'),
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
