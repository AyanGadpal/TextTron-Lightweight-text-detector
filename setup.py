from setuptools import setup, find_packages

setup(
name='TextTron',
version='0.1',
author='Ayan Gadpal',
author_email='ayangadpal2@gmail.com',
packages = ['TextTron'],
license = "MIT",
description = ("TextTron is a simple light-weight image processing based text detector in document images."),
long_description=("TextTron is a simple light-weight image processing based text detector in document images."
	"TextTron detects text with the help of Contours applied on a pre-processed image."
	"This meant for fast text detection without using any machine learning or deep learning model."
	"Though this will not work well in scene text detection, only meant for document images"),
keywords = "Text Detection, lightweight Text Detection, Document Text Detector",
url = "https://github.com/AyanGadpal/TextTron-Lightweight-text-detector",
requires=['opencv_python','numpy'],
)