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
	return cv2.VideoCapture(cam_id)

def release_webcam(capture):
	capture.release()
	try:
		cv2.destroyAllWindows()
	except:
		print "There is no windows to destroy (such a beautiful system)"

def save_frame(capture, folder, filename):
	try:
		ret, frame = capture.read()
		cv2.imwrite(folder + filename, frame)  
		return True
	except:
		print "Cant save frame"
		return False

def main():
	cap = setup_webcam(1)
	save_frame(cap, "../data/", "teste2.jpg")
	release_webcam(cap)

main()
