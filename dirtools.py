# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:41:51 2020

@author: Yurii
"""
import shutil
import os

def create_directory(dir_name, classes):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    for i in classes:
        os.makedirs(os.path.join(dir_name, i))