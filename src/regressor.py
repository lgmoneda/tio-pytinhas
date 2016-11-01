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

### Make some noooise
import pyttsx


def loadModel():
	input_shape = (3, 120, 160)

	model = Sequential()
	model.add(Convolution2D(32, 3, 3, input_shape=input_shape))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(32, 3, 3))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(64, 3, 3))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten()) 
	model.add(Dense(64))
	model.add(Activation('linear'))
	model.add(Dropout(0.5))
	model.add(Dense(1))

	model.load_weights("regressor3.h5")

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
	prediction = model.predict(img)[0]

	#print("Previsão: {0}".format(labels.keys()[labels.values().index(prediction)]))
	return int(abs(prediction))

def save_new_image(cap):

	filename = str(int(time.time())) + ".jpg"
	diretory = "../data/classifier_log/" 
	ret, frame = cap.read()
	print(frame.shape)
	save_frame(cap, diretory, filename)
	time.sleep(.5)

	filePath = diretory + "/" + filename
	return filePath

def returnImageArray(cap):
	ret, frame = cap.read()
	dim = (120, 160)
	resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)


	return frame

def returnSpeech(prediction):

	prediction = int(prediction)
	reais = prediction/100
	centavos = prediction%100
	msg2 = ""
	if reais < 1:
		return str(centavos) + " centavos."
	else:
		if reais == 1:
			msg1 = str(1) + " real"
		else:
			msg1 = str(reais) + " reais"
		if prediction%100 != 0:
			msg2 = " e " + str(centavos) + " centavos"

	return msg1 + msg2

### Fazendo com que previsoes sejam multiplos de 5
def closer_multiple(x, mult=5):
    value = mult * int(x / mult)
    if (x % mult) > mult/2.0:
        value += mult
    return value

if __name__ == '__main__':
	from collections import Counter
	engine = pyttsx.init()
	engine.setProperty('voice', "brazil")

	cap = setup_webcam(0)

	model = loadModel()
	key = "olá, amiguinho!"
	

	while(key != "q"):
		key = raw_input("Pressione enter para previsão ou q para sair")
		start = time.time()
		predictions = []
		for i in range(6):
			image_file = save_new_image(cap)
			#img = returnImageArray(cap)
			if i > 2:
				img = my_img_to_array(image_file)
				predictions.append(classify_single_image(model, img, verbose=True)) 
		print(predictions)
		prediction = sum(predictions)/len(predictions)
		prediction = closer_multiple(prediction)
		print("Previsão: {0}, em {1:.2f}s.".format(prediction, time.time() - start))
		engine = pyttsx.init()
		speech = returnSpeech(prediction)
		engine.say(speech, name=speech)
		engine.say(" ")
		engine.runAndWait()
		engine.stop()


	release_webcam(cap)
