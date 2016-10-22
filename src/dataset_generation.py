from webcam_funcs import *
import time

def gen_images_for_single_coin(cap, totaltime=300, live=False, rate=5):
	"""Takes labeled frames for single coin value from a capturer

		Receives a capturer to save frames from. A total time is passed
		as the time we'll be taking the frames, in a rate defined by a
		parameter. It can show the webcam image live while saving the
		frames. A regressive couting is shown in the screen to help
		user rearrange the coins, which need to keep their sum to be
		correctly labeled. The coin value is passed as an user input.
		You can put a lot of coins, but each one with the same value
		than others. Later, they'll be extracted individually. 

		Args:
			cap: the capturer object to get the frames from.
			totaltime: integer saying how many seconds we'll be saving 
						frames for that sum.
			live: a boolean for showing the webcam image while running.
			rate: integer seconds interval between saved frames.
		Returns:
			None 
	"""	
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
	gen_images_for_single_coin(cap, totaltime=150, live=True)
	release_webcam(cap)

main()