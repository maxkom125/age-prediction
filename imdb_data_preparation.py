# -*- coding: utf-8 -*-
"""
Created Jun 8 2020

@author: Maksym Komarov
"""
from tarfile import TarFile
import os
import shutil
import datetime as dt
from scipy.io import loadmat
from dirtools import create_directory

train_dir = 'second'          #path to locate sorted data
data_not_sorted = 'imdb_crop' #path to locate not sorted data
metadata_path = 'imdb_meta'   #path to locate metadata

classes = [str(i) for i in range(0, 91, 10)]

with TarFile("/content/gdrive/My Drive/Age_prediction/imdb_crop.tar","r") as mytar:
    mytar.extractall(data_not_sorted)

with TarFile("/content/gdrive/My Drive/Age_prediction/imdb_meta.tar","r") as mytar:
    mytar.extractall(metadata_path)

mat = loadmat(metadata_path + '/imdb/imdb.mat')
#mat['imdb'][0][0][0][0] #dob #days from January 1, 0000
#mat['imdb'][0][0][1][0] #yearphoto
#mat['imdb'][0][0][2][0] #path: array([array(['01/nm0000001_rm124825600_1899-5-10_1968.jpg'],

classes.append('notsorted')
create_directory(train_dir, classes)

nclasses = len(classes)
source_dir = data_not_sorted + '/imdb_crop'
dest_dir = train_dir

for i in range(len(mat['imdb'][0][0][1][0])):
  impath = str(mat['imdb'][0][0][2][0][i][0]) #path to image
  dob = dt.datetime.fromtimestamp(mat['imdb'][0][0][0][0][i] * 60 * 24 * 60).year - 1970 #date of birth
  apparent_age = mat['imdb'][0][0][1][0][i] - dob #YEARS OLD!
  directory = apparent_age // nclasses
  directory *= nclasses
  if directory < 0 or directory > 99:
    directory = 'notsorted'
  shutil.copy2(os.path.join(source_dir, impath), 
                    os.path.join(dest_dir, str(directory)))

shutil.rmtree(os.path.join(train_dir, 'notsorted'))
classes = classes[:-1]