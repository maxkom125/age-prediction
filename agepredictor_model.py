# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 2020

@author: Maksym Komarov
"""
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.applications.vgg16 import VGG16

def standard_agepredictor_model(output_units = 10, image_size = (256, 256), \
                                dense1units = 512, dense2units = None):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(image_size[0], image_size[1], 3))
    model = Sequential()
    model.add(base_model)
    model.add(Flatten())
    if dense1units != None:
        model.add(Dense(dense1units, activation='relu'))
        model.add(Dropout(0.5))
    if dense2units != None:
        model.add(Dense(dense2units, activation='relu'))
        model.add(Dropout(0.5))
    model.add(Dense(output_units, activation='softmax'))
    return model