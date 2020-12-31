# Author : Ayan Gadpal
# github : github.com/AyanGadpal
# Last Update : 12/16/2020

'''
	TextTron detect text with the help of Contours applied on a preprossed image. 
	This meant for fast text detection without using any machine learning or deep learning model. 
	Though this will not work well in scene text detection, only meant for document images
'''

import cv2
import numpy as np 
import operator

class TextTron:

	def __init__(self,img,low=177,high=255,yThreshold = 5,xThreshold = 2):
		
		assert isinstance(img, np.ndarray), "Image is empty or not in proper format,\n Only cv2 (numpy) image are accepted \n Use TextTron.from(pathtoimg) to read image directory from storage"
		

		self.img = img.copy()
		self.processedImg = self.preProcess(img,low,high)

		# Get the Countours
		contours , hierarchy = cv2.findContours(self.processedImg, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		# Get the BBox from the contours
		self.BBox = self.getBoundingBoxFromContour(contours)


		# Get Rows
		self.linesSet = self.clusterInRowsByY(yThreshold = yThreshold)
		# Get words in each row
		self.wordsSet =  self.clusterInWordsByX(xThreshold = xThreshold)
		
		self.plotImg, self.textBBox = self.getAndPlotTextBBox(self.img.copy(),self.wordsSet)

	def getTextBBox(self):
		return self.textBBox


	def preProcess(self,img,low,high):
		_,_,c = img.shape
		# if img is colored
		if c > 1:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Preprossing for the Countours 
		_, mask = cv2.threshold(img,low,high,cv2.THRESH_BINARY_INV)
		kernal = np.ones((2,2),np.uint8)
		dst = cv2.dilate(mask,kernal,iterations = 2)
		dst = cv2.bitwise_not(dst)
		return dst

	def getBoundingBoxFromContour(self,contours):
		rects = []
		width,height,_ = self.img.shape
		for cnt in contours:
			box = cv2.boundingRect(cnt)
			if cv2.contourArea(cnt) >= 60 :
				if (box[2] < (width*0.95)) and (box[3] < (height*0.95)):
				   rects.append(box)

		# Sort bounding rec	ts by Y and then X coordinate
		rects= sorted(rects , key = lambda x: (x[1], x[0]))
		return rects

	def clusterInRowsByY(self,yThreshold = 5):
		# intialise with first bounding box 
		LinesSet = []
		old = self.BBox[0][1]
		new = []
		new.append(self.BBox[0])

		# since first is already intialised
		for rect in self.BBox[1:]:
			# Next is within threshold range
			if (rect[1] - old) < yThreshold:
				new.append(rect)
			
			# New Row
			else:
				if new != []:
					# Finalise old row
					LinesSet.append(new)
				new = []
				# Start new row
				new.append(rect)

			# For next comparision
			old = rect[1]

		# Put the Last Remaining row 
		LinesSet.append(new)

		return LinesSet


	# Alternative Contructor
	# Set parameter by adjusting the trackbar
	# High value because changing it will produces many error, But you can try it if you want
	@classmethod
	def setParameters(cls,img):
		
		namedWindow = "TextTron Set Parameters"
		cv2.namedWindow(namedWindow)

		cv2.createTrackbar('low',namedWindow,0,250,lambda x:x)
		cv2.createTrackbar('yThreshold',namedWindow,0,50,lambda x:x)
		cv2.createTrackbar('xThreshold',namedWindow,0,50,lambda x:x)

		cv2.setTrackbarPos('xThreshold',namedWindow,5)
		cv2.setTrackbarPos('yThreshold',namedWindow,2)
		cv2.setTrackbarPos('low',namedWindow,177)
		
		# Note: Uncomment this if you want to set high value for thresholding too
		# It is commented because change it will produce some error
		# cv2.createTrackbar('high',namedWindow,100,255,lambda x:x)
		# cv2.setTrackbarPos('high',namedWindow,255)

		tt = cls(img,low=177,high=255,yThreshold=5,xThreshold=2)
		while True:
			low = cv2.getTrackbarPos('low',namedWindow)
			yThreshold = cv2.getTrackbarPos('yThreshold',namedWindow)
			xThreshold = cv2.getTrackbarPos('xThreshold',namedWindow)
			
			# Umcomment to enable high, and then please comment line below it, 
			# where the high is set manually to 255
			# high = cv2.getTrackbarPos('high',namedWindow)
			# tt = cls(img,low=low,high=255,yThreshold=yThreshold,xThreshold=xThreshold)

			tt = cls(img,low=low,high=255,yThreshold=yThreshold,xThreshold=xThreshold)
			plotImg = tt.plotImg
			cv2.imshow(namedWindow,plotImg)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cv2.destroyAllWindows()
		return tt 


	def clusterInWordsByX(self,xThreshold):
		WordsSet = []
		
		
		for line in self.linesSet:
			# Sort by x ,AGAIN
			line.sort(key = operator.itemgetter(0))

			# Intialise
			old = line[0][0]+line[0][2]
			new = []
			new.append(line[0])
			temp = []

			# Same logic as clusterInRowsByY
			for rect in line:
				if (rect[0] - old) < xThreshold:
					new.append(rect)
				else:
					if new != []:
						temp.append(new)
					new = []
					new.append(rect)
				old = rect[0]+rect[2]
			temp.append(new)
			WordsSet.append(temp)
		return WordsSet

	def getAndPlotTextBBox(self,oimg,WordsSet):
		TextBBox = []
		for line in WordsSet:
			for j,word in enumerate(line):
				# Re-Intialise for every WORD
				sxlist = []
				sylist = []
				exlist = []
				eylist = []
				for box in word:
					sxlist.append(box[0])
					sylist.append(box[1])
					exlist.append(box[2]+box[0])
					eylist.append(box[3]+box[1])

				minx = min(sxlist)
				miny = min(sylist)
				maxx = max(exlist)
				maxy = max(eylist)

				TextBBox.append([minx,miny,maxx-minx,maxy-miny])
				oimg = cv2.rectangle(oimg, (minx, miny), (maxx, maxy), (0, 0, 181), 2)
		
		return (oimg,TextBBox)	
