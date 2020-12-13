'''
contours
'''
import cv2
import numpy as np 
import operator

class TextTron:

	def __init__(self,img,low=177,high=255,yThreshold = 5,xThreshold = 8):
		
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

		print(self.textBBox)



	def preProcess(self,img,low,high):
		_,_,c = img.shape
		# if img is colored
		if c > 1:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Preprossing for the Countours 
		res, thresh = cv2.threshold(img,low,high,0)
		return thresh

	def getBoundingBoxFromContour(self,contours):
		rects = []
		width,height,_ = self.img.shape
		for cnt in contours:
			box = cv2.boundingRect(cnt)
			if (box[2] < (width*0.7)) and (box[3] < (height*0.7)):
			   rects.append(box)

		# Sort bounding rec	ts by Y and then x coordinate
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

	def clusterInWordsByX(self,xThreshold):
		WordsSet = []
		
		
		for line in self.linesSet:
			# Sort by x ,AGAIN
			line.sort(key = operator.itemgetter(0))

			# Intialise
			old = line[0][0]+line[0][2]
			naya = []
			naya.append(line[0])
			temp = []

			# Same logic as clusterInRowsByY
			for rect in line:
				if abs(rect[0] - old) < xThreshold:
					naya.append(rect)
				else:
					if naya != []:
						temp.append(naya)
					naya = []
					naya.append(rect)
				old = rect[0]+rect[2]
			temp.append(naya)
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



# # Intialial Magatmari
img = cv2.imread("Test10.png")
tt = TextTron(img)
# grayimg = cv2.imread("Test10.png",0) # i know
# width,height,_ = img.shape
# oimg = img.copy()

# # Preprossing for the Countours 
# res, thresh = cv2.threshold(grayimg,177,255,0)
# contours , hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# print("Number of contours = "+str(len(contours)))


# # rects.sort(key = getXFromRect)
# rects = getBoundingBoxFromContour(contours)

# # Sort bounding rects by Y and then x coordinate
# rects = sorted(rects, key = lambda x: (x[1], x[0]))

# LinesSet = clusterInRowsByY(rects)

# WordsSet =  clusterInWordsByX(LinesSet)

# oimg,_ = getAndPlotTextBBox(oimg,WordsSet)

# 	img = plotWordsWithDiffColor(img,WordsSet)

# cv2.imshow("WORDS",img)
# cv2.imshow("BBOX",oimg)


# cv2.waitKey(0)
# cv2.destroyAllWindows()