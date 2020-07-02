# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""

from keras.models import load_model
from keras.preprocessing import image

import numpy as np
from matplotlib import pyplot as plt

img_path = 'test/40/005642.jpg_face.jpg'
save_model_path = 'model'
image_size = (256, 256)

members = [load_model('model')]         #write path
classes = [i for i in range(0, 91, 10)] #CHECK testdata.class_indices!!!!
#classes = [int(get_key(traindata.class_indices, i)) for i in range(len(testdata.class_indices))]

def get_key(dictionary, argument):
  for key, arg in dictionary.items():
    if arg == argument:
      return key
  return "ERROR"

def ensemble_predictions(members, img_path, classes, show_image = True):
	img = image.load_img(img_path, target_size=image_size)
	testim = image.img_to_array(img)
	testim = np.expand_dims(testim, axis=0)
	# Предсказания
	yhats = [model.predict(testim)[0] for model in members]
	yhats = np.array(yhats)
	#summed = np.sum(yhats, axis=0) / len(members)
	# argmax - наиболее вероятный возраст
	#result = np.argmax(summed, axis=1)
	#result = get_key(traindata.class_indices, result)
	#classes = [int(get_key(traindata.class_indices, i)) for i in range(len(yhats[0]))]
	classes = np.array(classes, dtype = int)
	ans = 0
	#Матожидание
    #Итоговое значение - среднее по всем элементам ансамбля
	for yhat in yhats:
		result = np.multiply(yhat, classes)
		result = np.sum(result)
		#print(result)
		ans += result
	ans /= len(members)
	if show_image:
            #print(yhats) вероятности
            plt.imshow(img)
            plt.show()
	return np.round(ans, decimals = 2)

print(ensemble_predictions(members, img_path, classes))