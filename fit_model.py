# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.applications.vgg16 import VGG16
from keras.optimizers import Adam

def fit_model(traindata, valdata, fit_type = 'full', epochs = 1, \
              optimizer = Adam(learning_rate = 1e-5), \
              loss = 'categorical_crossentropy', image_size = (256, 256)): #fit_type mb fine_tuning
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(image_size[0], image_size[1], 3))
    model = Sequential()
    model.add(base_model)
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    #model.add(Dense(4096, activation='relu'))
    #model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))
    if fit_type == 'full':
        trainable = True
    else:
        #Тренируем только последние слои (fine tuning)
        trainable = False
    for layer in base_model.layers:
        if layer.name == 'block5_conv1':
            trainable = True
        layer.trainable = trainable
    #компилируем
    model.compile(optimizer = optimizer, loss = loss, metrics=["accuracy", "MAE"])
    #обучаем
    model.fit(traindata, epochs = epochs, validation_data = valdata)
    return model
