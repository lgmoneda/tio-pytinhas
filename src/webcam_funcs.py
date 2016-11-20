#from opencv site
import numpy as np
import cv2

def test_cam():
	# Zero for
	cap = cv2.VideoCapture(1)

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    # Our operations on the frame come here
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('frame',gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

def show_webcam(cap):
	"""Shows selected capturer image in a window.

	Shows the gray imagem captured by the deviced passed. To stop
	it, press q key.

	Args:
		cap: capturer object wich we'll show the content from.
	Returns:
		None
	"""
	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    # Our operations on the frame come here
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('frame',gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

def setup_webcam(cam_id=0):
	"""Setup the capturer

	Receive a webcam id and initialize a capturer with it.

	Args:
		cam_id: an int that defines which webcam will be used
				as capturer. Usually, 0 is the default embbeded
				webcam.
	Returns:
		A capturer object
	"""
	return cv2.VideoCapture(cam_id)

def release_webcam(capturer):
	"""Release capturer

	Release the device when we finish all we need from
	them, so it won't still busy.

	Args:
		capturer: a capturer object to be released.
	Returns:
		None 
	"""
	capturer.release()
	try:
		cv2.destroyAllWindows()
	except:
		print "There is no windows to destroy (such a beautiful system)"

def save_frame(capturer, folder, filename):
	"""Saves a single frame as image

	Saves a single frame from the passed capturer in a certain 
	directory.

	Args:
		capture: capturer object we're working with
		folder: string of the destiny diretory
		filename: string with the name for the image file
	Returns:
		A boolean about the procedure success
	"""
	try:
		ret, frame = capturer.read()
		cv2.imwrite(folder + filename, frame)  
		return True
	except:
		print "Cant save frame"
		return False

def main():
	cap = setup_webcam(1)
	save_frame(cap, "../data/", "teste2.jpg")
	release_webcam(cap)

#main()
