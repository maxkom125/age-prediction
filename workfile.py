# -*- coding: utf-8 -*-
"""
Created on Fri Jul 3 2020
@author: Maksym Komarov
"""
#IMDB data preparation
from imdb_data_preparation import prepare_imdb_data
#classes = [str(i) for i in range(0, 99, 1)]
path_tar_data     = "/content/gdrive/My Drive/Age_prediction/imdb_crop.tar"
path_tar_metadata = "/content/gdrive/My Drive/Age_prediction/imdb_meta.tar"

prepare_imdb_data(10, path_tar_data, path_tar_metadata, "IMDB_DATA")


#predict picture
from predict_picture import ensemble_predictions
from keras.models import load_model

img_path = 'test/40/005642.jpg_face.jpg'
save_model_path = 'model'

members = [load_model('model')]         #write path
classes = [i for i in range(0, 91, 10)] #CHECK testdata.class_indices!!!!

print(ensemble_predictions(members, img_path, classes))