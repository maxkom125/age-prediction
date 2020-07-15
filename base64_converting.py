# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 2020

@author: Maksym Komarov
"""
import base64 
from PIL import Image
import numpy as np
from io import BytesIO

def img_to_base64(path_to_image):
    image = open(path_to_image, 'rb') #open binary file in read mode
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read)
    return image_64_encode

def base64_to_img_array(image_64_encode, image_size = (256, 256)):
    image_64_decode = base64.decodebytes(image_64_encode) 
    im = Image.open(BytesIO(image_64_decode))
    im.thumbnail(image_size, Image.ANTIALIAS)
    im = np.array(im)
    im = np.expand_dims(im, axis=0)
    return im