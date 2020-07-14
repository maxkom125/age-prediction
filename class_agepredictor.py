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
import matplotlib.pyplot as plt

from model_log import ensemble_metrics
from model_log import plt_predict_real
from model_log import plt_age_error
from model_log import _get_real_predict

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

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
        self.__history   = None    
    
    def predict(self, img_path): #float age
        return ensemble_predictions(self.__members, img_path)
    
    def summary(self):
        for model in self.__members:
            model.summary()
        return  
    
    def __convert_dir(self, dir_to_convert = 'train'):
        if dir_to_convert == None:
            return [None for i in range(len(self.__members))]
        
        if type(dir_to_convert) == str:
            return [dir_to_convert for i in range(len(self.__members))]
            
        if len(dir_to_convert) != len(self.__members):
            print('The number of directories should be the same as the number of models or the only one')
            return [None for i in range(len(self.__members))]
        return dir_to_convert
    
    def train(self, train_dir = ['last_used_dir'], val_dir = None, epochs = 1,  fit_type = 'full',\
              optimizer = Adam(learning_rate = 1e-5), loss = 'categorical_crossentropy'):
        # Из какой папки берем данные
        if train_dir == ['last_used_dir']:
            if self.__train_dir == None:
                print('First usage of train method. Set train data dir')
                return
            else:
                train_dir = self.__train_dir
        
        if val_dir == ['last_used_dir']:
            if self.__val_dir == None:
                print('First usage of train method. Set valid data dir')
                return
            else:
                val_dir = self.__val_dir
        
        train_dir = self.__convert_dir(dir_to_convert = train_dir)
        val_dir   = self.__convert_dir(dir_to_convert = val_dir)
        
        if train_dir[0] == None:
            return
        
        self.__train_dir = train_dir
        self.__val_dir   = val_dir
        
        # Подготовка данных
        trdata = ImageDataGenerator(rotation_range = 10, zoom_range = [0.9, 1.1])
        traindata = []
        valdata   = []
        for i in range(len(self.__members)):
            traindata.append(trdata.flow_from_directory(directory = train_dir[i], \
                                                        target_size = self.__members[i].input_shape[1:3]))
            if val_dir[0] != None:
                vldata = ImageDataGenerator(rotation_range = 10, zoom_range = [0.9, 1.1])
                valdata.append(vldata.flow_from_directory(directory = val_dir[i], \
                                                        target_size = self.__members[i].input_shape[1:3]))
            else:
                valdata = val_dir
        
        #------------------ Область тренировки------------------
        model_number = 0
        self.__history = []
        for model in self.__members:
        
            if fit_type == 'full':
                trainable = True
                train_layer = True
            else:
                #Тренируем только последние слои (fine tuning)
                trainable = False
                train_layer = True            
        # Пояснения даны для fine tuning
            for i in range(len(model.layers) - 1, -1, -1): #только последние(улучшить)
                if type(model.layers[i]) in [Dense, Dropout]: #Последние полносвязные (и Dropout)
                    model.layers[i].trainable = train_layer
                else: #Когда дошли до первого не полносвзяного (и не Dropout) -- остальные не тренируем
                    train_layer = trainable
                    model.layers[i].trainable = train_layer
            # Компиляция
            model.compile(optimizer = optimizer, loss = loss, metrics = ["accuracy", "MAE"])
            # Обучаем
            self.__history.append( \
                    model.fit(traindata[model_number], epochs = epochs, validation_data = valdata[model_number]))
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
    
    def history(self):
        if self.__history == None:
            print('Empty history')
            return
        for history in self.__history:
            print(history.history.keys())
            # summarize history for accuracy
            plt.plot(history.history['accuracy'])
            plt.plot(history.history['val_accuracy'])
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            plt.show()
            # summarize history for loss
            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            plt.show()
        return
    
    def __get_testdata(self, from_dir):   
        tsdata = ImageDataGenerator()
        testdata = tsdata.flow_from_directory(directory = from_dir,  target_size = self.__members[0].input_shape[1:3])
        return testdata
    
    def metrics(self, test_dir):
        testdata = self.__get_testdata(test_dir)
        print(ensemble_metrics(self.__members, testdata))
        real, predict = _get_real_predict(self.__members, testdata.filepaths)
        print('age MAE:', mean_absolute_error(real, predict))
        print('R2: ', r2_score(real, predict))
        return
        
    def plt_predict_real(self, test_dir):
        testdata = self.__get_testdata(test_dir)
        plt_predict_real(self.__members, testdata.filepaths)
        return
    
    def plt_age_error(self, test_dir):
        testdata = self.__get_testdata(test_dir)
        plt_age_error(self.__members, testdata.filepaths)
        return
        
