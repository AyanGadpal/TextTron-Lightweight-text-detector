from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
name='TextTron',
version='0.42',
author='Ayan Gadpal',
author_email='ayangadpal2@gmail.com',
packages = ['TextTron'],
license = "MIT",
description = ("TextTron is a simple light-weight image processing based text detector in document images."),
long_description_content_type='text/markdown',
long_description=long_description,
keywords = "Text Detection, lightweight Text Detection, Document Text Detector",
url = "https://github.com/AyanGadpal/TextTron-Lightweight-text-detector",
requires=['opencv_python','numpy'],
)