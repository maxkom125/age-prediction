# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
from keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt

def ensemble_predictions(members, img_path, show_image = False, image_size = (256, 256)):
    img = image.load_img(img_path, target_size=image_size)
    testim = image.img_to_array(img)
    testim = np.expand_dims(testim, axis=0)
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
    if show_image:
        #print(yhats) вероятности
        plt.imshow(img)
        plt.show()
    return np.round(ans, decimals = 2)