# -*- coding: utf-8 -*-
import os
import setuptools

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

with open("README.md") as f:
    README = f.read()

with open("LICENSE.txt") as f:
    LICENSE = f.read()

VERSION_PATH = os.path.join(os.path.dirname(__file__), "src", "VERSION.txt")
with open(VERSION_PATH, "r") as version_file:
    VERSION = version_file.read().strip()

setuptools.setup(
    name="model-and-simulate",
    version="0.1.0",
    description="Student projects to learn modeling and simulating.",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=(
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ),
    author="Tom Krueger",
    author_email="tomtuamnuq@users.noreply.github.com",
    url="https://github.com/tomtuamnuq/model_and_simulate",
    license=LICENSE,
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=REQUIREMENTS,
    python_requires=">=3.9",
)
