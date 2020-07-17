# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
import numpy as np

def ensemble_predictions(members, testim):
    # Предсказания
    yhats = [model.predict(testim)[0] for model in members]
    yhats = np.array(yhats)
    period = 100 // len(yhats[0])
    classes = [str(i) for i in range(0, 100, period)]
    classes = sorted(classes)
    classes = np.array(classes, dtype = int)
    ans = 0
    #Матожидание
    #Итоговое значение - среднее по всем элементам ансамбля
    for yhat in yhats:
        result = np.multiply(yhat, classes)
        result = np.sum(result)
        ans += result
    ans /= len(members)
    return np.round(ans, decimals = 2)