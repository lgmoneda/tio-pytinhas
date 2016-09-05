from webcam_funcs import *
import time

def gen_images_for_single_coin(cap, totaltime=300, live=False, rate=5):
	value = raw_input("What's the coin value?")
	folder = "../data/" + str(value) + "/"
	start = time.time()
	end = time.time()

	while(end - start < totaltime):
		end = time.time()
		filename = str(value) + "_" + str(int(end)) + ".jpg"
		ret, frame = cap.read()
		if int(end)%rate == 0:
			save_frame(cap, folder, filename)
		if live:			
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			cv2.imshow('frame',gray)
			cv2.waitKey(1)

def main():
	cap = setup_webcam(1)
	gen_images_for_single_coin(cap, totaltime=30, live=True)
	release_webcam(cap)

main()