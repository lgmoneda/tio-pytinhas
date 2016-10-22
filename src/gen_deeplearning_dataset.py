from webcam_funcs import *
import time
import os

def gen_images_for_single_coins_sum(cap, totaltime=300, live=False, 
									rate=5):
	"""Takes labeled frames for coins sum from a capturer

	Receives a capturer to save frames from. A total time is passed
	as the time we'll be taking the frames, in a rate defined by a
	parameter. It can show the webcam image live while saving the
	frames. A regressive couting is shown in the screen to help
	user rearrange the coins, which need to keep their sum to be
	correctly labeled. The sum is passed as an user input.

	Args:
		cap: the capturer object to get the frames from.
		totaltime: integer saying how many seconds we'll be saving 
					frames for that sum.
		live: a boolean for showing the webcam image while running.
		rate: integer seconds interval between saved frames.
	Returns:
		None 
	"""
	value = raw_input("What's the coins sum?")
	diretory = "../data/deeplearning/" + str(value) + "/"
	diretoryAll = "../data/deeplearning/all/"

	font = cv2.FONT_HERSHEY_SIMPLEX

	if not os.path.exists(diretory):
		os.makedirs(diretory)

	start = time.time()
	end = time.time()
	rate += 1
	while(end - start < totaltime):
		end = time.time()
		filename = str(value) + "_" + str(int(end)) + ".jpg"
		ret, frame = cap.read()
		text = str(rate - int(end)%(rate) )
		if int(end)%(rate) == 0:
			save_frame(cap, diretory, filename)
			save_frame(cap, diretoryAll, filename)
			text = "olha o passarinho!"
		if live:	
			cv2.putText(frame, text, (40, 40), font, 1, (0, 0, 255), 2)		
			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#cv2.imshow('frame',gray)
			cv2.imshow('frame',frame)
			cv2.waitKey(1)

def main():
	cap = setup_webcam(2)
	gen_images_for_single_coins_sum(cap, totaltime=180, live=True)
	release_webcam(cap)

main()