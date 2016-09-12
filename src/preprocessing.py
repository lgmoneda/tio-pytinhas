import cv2
import numpy as np
import os, sys

def extract_coins(file_, folder):
	"""Detect round objects in a image and extract as new images

	Takes a image file, find all round objects and extract them as
	new images. Uses opencv function HoughCircles to detect circles.
	Then make a new image file using center position and radius info
	about it, save in a folder called "extracted", which is in the 
	folder passed.

	Args:
		file_: string with image file name.
		folder: the folder it is in and where the extracted folder
				will be.
	Returns:
		None.

	"""
	image = cv2.imread(folder + file_)
	output = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#Add border
	border_size = 10
	BLACK = [0, 0, 0]
	image = cv2.copyMakeBorder(image,border_size,border_size,border_size,border_size,cv2.BORDER_CONSTANT,value=BLACK)

	# detect circles in the image
	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 0.4, 50)
	coins = [] 
	i = 0
	# ensure at least some circles were found
	if circles is not None:
		
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
	 
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			i += 1
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)	

			r += 8
			coin = image[y-r:y+r,x-r:x+r]
			#coin = image[y-int(r/2.0):y+int(r/2.0), x-int(r/2.0):x+int(r/2.0)]
			#coin = image[y-100:y+100, x-100:x+100]
			print r
			coins.append(cv2.imwrite(folder + "/extracted/" + file_[:-4] + "_coin_" + str(i) + ".jpg", coin))
	 
		# show the output image
		cv2.imshow("output", np.hstack([image, output]))
		cv2.waitKey(0)
	
def extract_from_all_raw():
	"""extract coins from all raw images

	Goes through all raw images folders and extract all the detected
	coins from them. 

	Args:
		None
	Returns
		None
	"""
	values = ["1", "5", "10", "25", "50", "100"]
	for value in values:
		folder = "../data/" + value + "/"
		onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
		print "Valor da moeda: " + str(value)
		print onlyfiles

		for file_ in onlyfiles:
			extract_coins(file_, folder)

def main():
	#extract_from_all_raw()
	extract_coins("10_1473117300.jpg", "../data/10/")

main()