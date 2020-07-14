# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.applications.vgg16 import VGG16
from keras.optimizers import Adam
from keras.models import load_model

#??????????????????????? название неудачно -> class MyModel c model = 'standard' методы compile и fit
def fit_model(traindata, valdata = None, epochs = 1, model = 'standard',  fit_type = 'full',\
              optimizer = Adam(learning_rate = 1e-5), dense1units = 512, dense2units = None, \
              loss = 'categorical_crossentropy', image_size = (256, 256), \
              output_units = 'auto'): #fit_type mb fine_tuning
    if model == 'standard':
        if output_units == 'auto':
            output_units = len(traindata.class_indices)
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
    elif type(model) == str:
        model = load_model(model)
        
    if fit_type == 'full':
        trainable = True
    else:
        #Тренируем только последние слои (fine tuning)
        trainable = False
    for layer in base_model.layers: #???????????????????только последние(улучшить)
        if layer.name == 'block5_conv1':
            trainable = True
        layer.trainable = trainable
    #компилируем
    model.compile(optimizer = optimizer, loss = loss, metrics = ["accuracy", "MAE"])
    #обучаем
    model.fit(traindata, epochs = epochs, validation_data = valdata)
    return model
