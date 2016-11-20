#encoding=utf-8
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.callbacks import EarlyStopping
import numpy as np
from webcam_funcs import *
import time
import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import cv
### Make some noooise
import pyttsx


def loadModel():
	input_shape = (3, 120, 160)

	model = Sequential()
	model.add(Convolution2D(32, 3, 3, input_shape=input_shape, dim_ordering='th'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(32, 3, 3, dim_ordering='th'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(64, 3, 3, dim_ordering='th'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten()) 
	model.add(Dense(64))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(5))
	model.add(Activation('softmax'))

	model.load_weights("classificador_5.h5")

	return model

def loadModel2():
	input_shape = (3, 120, 160)

	model = Sequential()
	model.add(Convolution2D(64, 3, 3, input_shape=input_shape))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(64, 3, 3))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(128, 3, 3))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(256, 3, 3))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten()) 
	model.add(Dense(64))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(5))
	model.add(Activation('softmax'))

	model.load_weights("classificador2_2.h5")

	return model


def my_img_to_array(image_file):

    #Medidas originais 
    image_width = 640
    image_height = 480
    ratio = 4
    
    image_width = image_width / ratio
    image_height = image_height / ratio

    channels = 3
    nb_classes = 1

    my_image = np.ndarray(shape=(1, channels, image_height, image_width),
                         dtype=np.float32)

    ### PIL image
    img = load_img(image_file)  
    img.thumbnail((image_width, image_height))
    x = img_to_array(img)  

    ### Normalizando
    x = (x - 128.0) / 128.0
    my_image[0] = x

    
    return my_image

def classify_single_image(model, img, verbose=False):
	labels = {"5": 0, "10": 1, "25": 2, "50":3, "100":4} 
	probabilities = model.predict(img)
	if verbose:
		print("Probabilidades: ")
		for i in range(len(probabilities[0])):
			print(str(labels.keys()[labels.values().index(i)]) + ": {0:.4f}".format(probabilities[0][i]))
	prediction = np.argmax(probabilities)
	#print("Previsão: {0}".format(labels.keys()[labels.values().index(prediction)]))
	return labels.keys()[labels.values().index(prediction)]

def save_new_image(cap):

	#filename = str(int(time.time())) + ".jpg"
	filename = "minha_imagem.jpg"
	diretory = "../data/classifier_log/" 
	#ret, frame = cap.read()

	#ff = np.reshape(frame, (3, 480, 640))

	save_frame(cap, diretory, filename)
	time.sleep(.5)

	filePath = diretory + filename
	return filePath

def cam_to_array(cap):

	ret, frame = cap.read()
	print("frame shape: ")
	print(frame.shape)
	ff = np.reshape(frame, (3, 480, 640))
	img = array_to_img(ff)

	image_width = 640
	image_height = 480
	ratio = 4

	channels = 3
	image_width = image_width / ratio
	image_height = image_height / ratio

	

	img.thumbnail((image_width, image_height))
	x = img_to_array(img)  
	my_image = np.ndarray(shape=(1, channels, image_height, image_width),
             				dtype=np.float32)
	### Normalizando
	x = (x - 128.0) / 128.0
	#x = np.reshape(x, (1, channels, image_height, image_width))
	my_image[0] = x

	time.sleep(.5)

	return my_image

def cam_to_array2(cap):

	ret, frame = cap.read()
	#print("frame shape: ")
	#print(frame.shape)
	#time.sleep(.5)
	#ret, frame = cap.read()
	#time.sleep(.5)
	#ret, frame = cap.read()

	ff = np.reshape(frame, (3, 120, 160))

	image_width = 640
	image_height = 480
	ratio = 4

	channels = 3
	image_width = image_width / ratio
	image_height = image_height / ratio	
	my_image = np.ndarray(shape=(1, channels, image_height, image_width),
	             				dtype=np.float32)

	my_image[0] = ff
	time.sleep(2)
	return my_image
	



def returnSpeech(prediction):
	speechs = {"5": "Cinco centavos",
			   "10": "Dez centavos",
			   "25": "Vinte e cinco centavos",
			   "50": "Cinquenta centavos",
			   "100": "Um real"}
	return speechs[prediction]

if __name__ == '__main__':
	from collections import Counter
	engine = pyttsx.init()
	engine.setProperty('voice', "brazil")

	cap = setup_webcam(0)
	cap.open(0)
	#cap.set(cv.CV_CAP_PROP_FRAME_WIDTH,160)
	#cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT,120)

	model = loadModel()
	key = "olá, amiguinho!"
	predictions = []
	# for k in range(100):
	# #while(True):
	# 	#key = raw_input("Pressione enter para previsão ou q para sair")
	# 	start = time.time()
	# 	#predictions = []
	# 	"""
	# 	for i in range(5):
	# 		#img = cam_to_array2(cap)
	# 		if i > 2:
	# 			#save_new_image(cap)
	# 			img = cam_to_array2(cap)
	# 			predictions.append(classify_single_image(model, img, verbose=True)) 
	# 	"""
	# 	predictions = []
	# 	cap = setup_webcam(0)
	# 	cap.open(0)
	# 	for i in range(5):
	# 		image_file = save_new_image(cap)
	# 		time.sleep(.5)
	# 		if i > 2:
	# 			img = my_img_to_array(image_file)
	# 			predictions.append(classify_single_image(model, img, verbose=True)) 
	# 	print(predictions)
	# 	release_webcam(cap)
		
	# 	prediction = Counter(predictions[:]).most_common(1)[0][0]

	# 	#cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 160)
	# 	#cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
		
	# 	#img = cam_to_array2(cap)
	# 	#predictions.append(classify_single_image(model, img, verbose=True)) 
	# 	#print(predictions)
	# 	#prediction = Counter(predictions[:]).most_common(1)[0][0]
	# 	print("Previsão: {0}, em {1:.2f}s.".format(prediction, time.time() - start))
	# 	engine = pyttsx.init()
	# 	speech = returnSpeech(prediction)
	# 	engine.say(speech, name=speech)
	# 	engine.say(" ")
	# 	engine.runAndWait()
	# 	engine.stop()
	# 	time.sleep(5)

	predictions = []
	#cap = setup_webcam(1)
	#cap.open(1)
	start = time.time()
	imgago = cam_to_array(cap)
	image_file = save_new_image(cap)
	img = my_img_to_array(image_file)
	predictions.append(classify_single_image(model, img, verbose=True)) 
	time.sleep(.5)

	#img = my_img_to_array(image_file)
	#predictions.append(classify_single_image(model, img, verbose=True)) 
	print(predictions)
	
	prediction = Counter(predictions[:]).most_common(1)[0][0]
	print("Previsão: {0}, em {1:.2f}s.".format(prediction, time.time() - start))
	engine = pyttsx.init()
	speech = returnSpeech(prediction)
	engine.say(speech, name=speech)
	engine.say(" ")
	engine.runAndWait()
	engine.stop()

	engine.say("Terminando o programa")
	engine.runAndWait()
	release_webcam(cap)
