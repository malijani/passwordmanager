#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passman",
    version="0.0.1",
    author="Mohammad Alijani",
    author_email="AlijaniAlijanvandMohammad@gmail.com",
    description="Password manager tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malijani/passwordmanager",
    packages=['passman'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
