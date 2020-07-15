# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
from keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt

from base64_converting import base64_to_img_array

def ensemble_predictions(members, img, show_image = False):
    image_size = members[0].input_shape[1:3]
    if type(img) == bytes:
        testim = base64_to_img_array(img, image_size)
    else:
        if type(img) == str: #если картинка подана в виде пути
            img = image.load_img(img, target_size=image_size)
        if type(img) != np.ndarray: #если картинка загружена keras.preprocessing.image
            testim = image.img_to_array(img)
            testim = np.expand_dims(testim, axis=0)
        else:
            testim = img
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
    if show_image and type(img) != np.ndarray: #только если загружена в необработанном формате
        #print(yhats) вероятности
        plt.imshow(img)
        plt.show()
    return np.round(ans, decimals = 2)