# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:45:15 2020

@author: Maksym Komarov
"""
import requests
from base64_converting import img_path_to_base64

x = {'Harry Potter' : img_path_to_base64('E:/Maksym/GitHub/age-prediction/images/Harry_Potter.jpg'), 'Hermione Granger' : img_path_to_base64('E:/Maksym/GitHub/age-prediction/images/Hermione_Granger.jpg')}
response = requests.post('http://127.0.0.1:5000/', data = x)
jsonobj = response.json()
print(jsonobj)

