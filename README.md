# TextTron-Lightweight-text-detector
<img align="right" src="media/demo.gif" /> 

## 1. Introduction

TextTron is a simple light-weight image processing based text detector in document images. 
TextTron detect text with the help of Contours applied on a preprossed image. This meant for fast text detection without using any machine learning or deep learning model.
Though this will not work well in scene text detection, only meant for document images 

## 2. Quick Start
#### 1. Requirements: numpy & opencv-python
* `pip install numpy`
* `pip install opencv-python`
#### 2. Install the package 
```
$pip install TextTron
```

<b>Code is developed under following library dependencies</b> <br>
OpenCV = 4.1.2 <br>
NumPy = 1.17 <br>



## 3. Usage
### 3.1 API


i. Import the neccessary libraries and read the image
```
import cv2
import TextTron
img = cv2.imread(PATH)
```
ii. Pass the numpy or cv2 image to the TextTron 
```
TT = TextTron(img) 
TT = TextTron(img, low=196,high=255,yThreshold=15,xThreshold=2) # Change this till you get good result
```
iii. Get the text bounding boxes
```
tbbox = TT.textBBox
``` 

<img align="right" src="media/GUI.gif" /> 

iv. Get the ploted image (optional)
```
plotImg = TT.plotImg
``` 
v. If you want to set/decide best parameter for your case (optional)
```
TextTron.setParameters(img)
```
## 4. Contact
Ayan Gadpal : ayangadpal2 [at] gmail [dot] com <br>

## 5. References 
1. Y. Liu, S. Goto, T. Ikenaga, "A Contour-Based Robust Algorithm for Text Detection in Color Images", IEICE TRANS. INF. & SYST., VOL.E89–D, NO.3 MARCH 2006 
2. Giotis, A., Gerogiannis, D., Nikou, C.: Word Spotting in Handwritten Text Using Contour-Based Models. In: Frontiers in Handwriting Recog. (ICFHR), 2014 14th Int. Conf. on. pp. 399{404 (Sept 2014), doi:10.1109/ICFHR.2014.73
