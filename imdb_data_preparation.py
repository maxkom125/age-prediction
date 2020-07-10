# -*- coding: utf-8 -*-
"""
Created Jun 8 2020

@author: Maksym Komarov
"""
#Подготовка датасета IMDB. Классы - целые числа в промежутке [0, 99]
#Любое количество классов с равными промежутками между ними
from tarfile import TarFile
import os
import shutil
import datetime as dt
from scipy.io import loadmat

#import sys
#sys.path.insert(1, '/content/gdrive/My Drive/Age_prediction') #path to dirtools.py
from dirtools import create_directory
from dirtools import get_agedir
from dirtools import get_classes

def prepare_imdb_data(period, path_tar_data, path_tar_metadata, \
        sorted_data_locate, not_sorted_data_locate = None, metadata_locate = None):
    classes = get_classes(period)
    if not_sorted_data_locate == None:
      not_sorted_data_locate = 'data_not_sorted_workfile_will_be_deleted'
    if metadata_locate == None:
      metadata_locate = 'metadata_workfile_will_be_deleted'

    train_dir = sorted_data_locate              #path to locate sorted data
    data_not_sorted = not_sorted_data_locate    #path to locate not sorted data
    metadata_path = metadata_locate             #path to locate metadata

    with TarFile(path_tar_data,"r") as mytar:
        mytar.extractall(data_not_sorted)

    with TarFile(path_tar_metadata,"r") as mytar:
        mytar.extractall(metadata_path)

    mat = loadmat(metadata_path + '/imdb/imdb.mat')
    #mat['imdb'][0][0][0][0] #dob #days from January 1, 0000
    #mat['imdb'][0][0][1][0] #yearphoto
    #mat['imdb'][0][0][2][0] #path: array([array(['01/nm0000001_rm124825600_1899-5-10_1968.jpg'],

    create_directory(train_dir, classes)


    source_dir = data_not_sorted + '/imdb_crop'
    dest_dir = train_dir

    for i in range(len(mat['imdb'][0][0][1][0])):
      impath = str(mat['imdb'][0][0][2][0][i][0]) #path to image
      dob = dt.datetime.fromtimestamp(mat['imdb'][0][0][0][0][i] * 60 * 24 * 60).year - 1970 #date of birth
      apparent_age = mat['imdb'][0][0][1][0][i] - dob #YEARS OLD!
      if apparent_age >= 0 and apparent_age <= 99:
        directory = get_agedir(apparent_age, classes)
        shutil.copy2(os.path.join(source_dir, impath), 
                          os.path.join(dest_dir, directory))

    if os.path.exists('data_not_sorted_workfile_will_be_deleted'):
        shutil.rmtree('data_not_sorted_workfile_will_be_deleted')
    if os.path.exists('metadata_workfile_will_be_deleted'):
        shutil.rmtree('metadata_workfile_will_be_deleted')