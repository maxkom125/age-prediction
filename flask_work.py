# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:45:15 2020

@author: Yurii
"""
import requests
#import sys
#sys.path.insert(1, 'E:/Maksym/GitHub/age-prediction') #path to files
from base64_converting import img_path_to_base64
#POST
x = {'Harry Potter' : img_path_to_base64('E:/Maksym/GitHub/age-prediction/images/Harry_Potter.jpg'), 'Hermione Granger' : img_path_to_base64('E:/Maksym/GitHub/age-prediction/images/Hermione_Granger.jpg')}
#x = img_path_to_base64('E:/Maksym/Cats_vs_dogs/dog.5465.jpg')
response = requests.post('http://127.0.0.1:5000/', data = x)
#GET
response = requests.get('http://127.0.0.1:5000/')
jsonobj = response.json()
jsonobj = jsonobj["age"]
print(jsonobj)

