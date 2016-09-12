import cv2
import numpy as np
import os, sys
# load the image, clone it for output, and then convert it to grayscale

def extract_coins(file_, folder):
	image = cv2.imread(folder + file_)
	output = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#Add border
	#border_size = 10
	#BLACK = [0, 0, 0]
	#image = cv2.copyMakeBorder(image,border_size,border_size,border_size,border_size,cv2.BORDER_CONSTANT,value=BLACK)

	# detect circles in the image
	#circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 0.4, 50)
	
	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 150,
              param1=1,
              param2=5,
              minRadius=20,
              maxRadius=300)

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

			

			#r += 8
			#coin = image[y-r:y+r,x-r:x+r]
			
			#coin = image[y-int(r/2.0):y+int(r/2.0), x-int(r/2.0):x+int(r/2.0)]
			#coin = image[y-100:y+100, x-100:x+100]
			
			#print r
			#coins.append(cv2.imwrite(folder + "/extracted/" + file_[:-4] + "_coin_" + str(i) + ".jpg", coin))
	 
		# show the output image
		cv2.imshow("output", np.hstack([image, output]))
		cv2.waitKey(0)
		


def main():
	#values = ["1", "5", "10", "25", "50", "100"]
	values = ["10"]
	for value in values:
		folder = "../data/" + value + "/"
		onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
		file_ = "10_1473117180.jpg"
		extract_coins(file_, folder)
		#print "Valor da moeda: " + str(value)
		#print onlyfiles
		"""
		for file_ in onlyfiles:
			extract_coins(file_, folder)
		"""
main()