# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 2020

@author: Maksym Komarov
"""
from keras.models import load_model
from predict_picture import ensemble_predictions
from numpy import ndarray
from keras.engine.sequential import Sequential as standardmodel

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
        for path in models:
            ans.append(__age_predictor_get_model(path))
    else:
        ans = [__age_predictor_get_model(models)]
    return ans

class AgePredictor:
    def __init__(self, models = 'modelFINAL0'):
        self.__members = get_models(models)
            
    
    def predict(self, img_path): #float age
        return ensemble_predictions(self.__members, img_path)
        
