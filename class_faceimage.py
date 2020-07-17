# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 17:01:15 2020

@author: Maksym Komarov
"""
from matplotlib import pyplot as plt
from base64_converting import base64_to_img_array
from base64_converting import img_to_base64
from keras.preprocessing import image

class FaceImage:
    def __init__(self, img, image_size = (256, 256)):
        self.image_size = image_size
        
        if type(img) == bytes:
            self.base64 = img
        elif type(img) == str: #если картинка подана в виде пути
            self.base64 = img_to_base64(img)
            
        return
        
        
    def img_array(self):
        return base64_to_img_array(self.base64, self.image_size)
                
    
    def show_image(self): #только если загружена в необработанном формате
        img_array = self.img_array(self.base64)
        img = image.array_to_img(img_array[0,:,:,:])
        plt.imshow(img)
        plt.show()
        return
        
    