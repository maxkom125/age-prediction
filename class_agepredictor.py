# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 2020

@author: Maksym Komarov
"""
from keras.models import load_model
from predict_picture import ensemble_predictions
from numpy import ndarray
from keras.engine.sequential import Sequential as standardmodel
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from agepredictor_model import standard_agepredictor_model

from keras.layers.core import Dense
from keras.layers.core import Dropout

from model_log import ensemble_metrics

def __age_predictor_get_model(model):
    if type(model) == str:
        ans = load_model(model)
    elif type(model) == standardmodel:
        ans = model
    else:
        print('Error init of AgePredictor: incorrect models: ', model)
        return -1
    return ans

def get_models(models):
    ans = []
    if type(models) in [list, ndarray]:
        for model in models:
            ans.append(__age_predictor_get_model(model))
    else:
        ans = [__age_predictor_get_model(models)]
    return ans

class AgePredictor:
    
    def __init__(self, models = standard_agepredictor_model(output_units = 10)):
        self.__members = get_models(models)
        self.__train_dir = None   
        self.__val_dir   = None
        self.history   = [None for i in range(len(self.__members))]
    
    def predict(self, faceimage): #float age
        return ensemble_predictions(self.__members, faceimage.img_array())
    
    def summary(self):
        for model in self.__members:
            model.summary()
        return  
    
    def train(self, train_dir = None, val_dir = None, n_model_to_train = 'all', \
              epochs = 1,  fit_type = 'full', optimizer = Adam(learning_rate = 1e-5), \
              loss = 'categorical_crossentropy'):
        
        if n_model_to_train == 'all':
            model_ref = [i for i in range(len(self.__members))]
        else:
            model_ref = [n_model_to_train]
	
        # Из какой папки берем данные
        if train_dir == None:
            if self.__train_dir == None:
                print('First usage of train method. Set train data dir')
                return
            else:
                train_dir = self.__train_dir
        
        self.__train_dir = train_dir
        
        if val_dir == None:
            val_dir = self.__val_dir
        else:
            self.__val_dir = val_dir
         
        # Подготовка данных
        trdata = ImageDataGenerator(rotation_range = 10, zoom_range = [0.9, 1.1])
        traindata = trdata.flow_from_directory(directory = train_dir, \
                                               target_size = self.__members[model_ref[0]].input_shape[1:3])
        if val_dir != None:
            vldata = ImageDataGenerator(rotation_range = 10, zoom_range = [0.9, 1.1])
            valdata = vldata.flow_from_directory(directory = val_dir, \
                                                 target_size = self.__members[model_ref[0]].input_shape[1:3])
        else:
            valdata = val_dir
        
        #------------------ Область тренировки------------------
        model_number = 0
        for n_model in model_ref:
            model = self.__members[n_model]
        
            if fit_type == 'full':
                trainable = True
                train_layer = True
            else:
                #Тренируем только последние слои (fine tuning)
                trainable = False
                train_layer = True  
                
            # Пояснения даны для fine tuning
            for i in range(len(model.layers) - 1, -1, -1): # только последние(улучшить)
                if type(model.layers[i]) in [Dense, Dropout]: # Последние полносвязные (и Dropout)
                    model.layers[i].trainable = train_layer
                else: # Когда дошли до первого не полносвзяного (и не Dropout) -- остальные не тренируем
                    train_layer = trainable
                    model.layers[i].trainable = train_layer
                    
            # Компиляция
            model.compile(optimizer = optimizer, loss = loss, metrics = ["accuracy", "MAE"])
            # Обучение
            self.history[n_model] = model.fit(traindata, epochs = epochs, \
                                          validation_data = valdata)
            model_number += 1

    def save_models(self, save_to = 'default'):
        if save_to == 'default':
            save_to = ['model' + str(i) for i in range(len(self.__members))]
        i = 0
        if len(save_to) != len(self.__members):
            print('The number of models is not equal to the number of paths to save. Saved by default')
        for model in self.__members:
            model.save(save_to[i])
            i += 1
        return
    
    
    def __get_testdata(self, from_dir):   
        tsdata = ImageDataGenerator()
        testdata = tsdata.flow_from_directory(directory = from_dir,  target_size = self.__members[0].input_shape[1:3])
        return testdata
    
    
    def metrics(self, test_dir):
        testdata = self.__get_testdata(test_dir)
        return ensemble_metrics(self.__members, testdata)
        
