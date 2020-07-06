# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:41:51 2020

@author: Yurii
"""
import shutil
import os
from math import floor

def create_directory(dir_name, classes):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    for i in classes:
        os.makedirs(os.path.join(dir_name, i))
        
def get_agedir(age, classes):
    if age < 0 or age > 99:
      return 'notsorted'
    period = 100 // len(classes)
    age /= period
    age = floor(age)
    age *= period
    return str(age)

def get_classes(period):
    return [str(i) for i in range(0, 99, period)]