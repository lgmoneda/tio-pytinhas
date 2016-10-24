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
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(5))
	model.add(Activation('softmax'))

	model.load_weights("classificador.h5")

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

   
    img = load_img(image_file)  # this is a PIL image
    img.thumbnail((image_width, image_height))
    #img = img.convert('L')
    # Transformando em Numpy Array
    x = img_to_array(img)  
    #print(x.shape)
    #x = x.reshape((1,) + x.shape)
    # Normalizando
    x = (x - 128.0) / 128.0
    my_image[0] = x
    #i += 1
    #if i % 100 == 0:
        #print("%d images to array" % i)
    
    return my_image

def classify_single_image(model, img):
	labels = {"5": 0, "10": 1, "25": 2, "50":3, "100":4} 
	prediction = np.argmax(model.predict(img))
	print("Previsão: {0}".format(labels.keys()[labels.values().index(prediction)]))
	return labels.keys()[labels.values().index(prediction)]

def save_new_image(cap):

	filename = str(int(time.time())) + ".jpg"
	diretory = "../data/classifier_log/" 
	ret, frame = cap.read()
	save_frame(cap, diretory, filename)

	filePath = diretory + "/" + filename
	return filePath

if __name__ == '__main__':

	cap = setup_webcam(1)

	model = loadModel()
	key = "olá, amiguinho!"
	while(key != "q"):
		key = raw_input("Pressione enter para previsão ou q para sair")
		image_file = save_new_image(cap)
		img = my_img_to_array(image_file)
		prediction = classify_single_image(model, img)


	release_webcam(cap)
