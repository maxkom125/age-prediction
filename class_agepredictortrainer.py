# -*- coding: utf-8 -*-
"""
Created on Fri Jul 3 2020
@author: Maksym Komarov
"""
from fit_model import fit_model
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from class_agepredictor import get_models

class TrainerAgePredictor:
    
    def __init__(self, models = 'modelFINAL0'):
        if models != -1:
            self.__members = get_models(models)
        
    def train(self, data_path, image_size = (256, 256), optimizer = Adam(learning_rate = 1e-5), \
              loss = 'categorical_crossentropy', epochs = 1):
        #картинки
        # Каталог с данными для обучения
        train_dir = data_path
        # Каталог с данными для проверки
        #val_dir = 'valid'
        
        trdata = ImageDataGenerator(rotation_range=10, zoom_range = [0.9, 1.1])
        #vldata = ImageDataGenerator(rotation_range=10, zoom_range = [0.9, 1.1])
        
        traindata = trdata.flow_from_directory(directory = train_dir, target_size=image_size)
        #valdata   = vldata.flow_from_directory(directory = val_dir,   target_size=image_size)
        #print(traindata.class_indices)
        
        self.__members = fit_model(traindata, valdata = None, fit_type = 'full', epochs = epochs, \
              optimizer = optimizer, dense1units = 512, dense2units = None, \
              loss = loss, image_size = image_size, output_units = 'auto')
        return
    
    #def save_model(self, save_model_path = ['model' + str(i) for i in range(len(self.__members))]):
        #self.__members.save(save_model_path)