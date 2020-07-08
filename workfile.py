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

#data_preparation
from data_preparation import prepare_zip_data
path_zip_data = '/content/gdrive/My Drive/Age_prediction/appa-real-release.zip'
prepare_zip_data(10, path_zip_data)

#fit_model
from fit_model import fit_model
from keras.preprocessing.image import ImageDataGenerator
save_model_path = 'model'
image_size = (256, 256)
#optimizer = Adam(learning_rate = 1e-5)
#loss = 'categorical_crossentropy'
#epochs = 1
#картинки
# Каталог с данными для обучения
train_dir = 'train'
# Каталог с данными для проверки
val_dir = 'valid'
# Каталог с данными для тестирования
#test_dir = 'test'

trdata = ImageDataGenerator(rotation_range=10, zoom_range = [0.9, 1.1])
vldata = ImageDataGenerator(rotation_range=10, zoom_range = [0.9, 1.1])
#tsdata = ImageDataGenerator()

traindata = trdata.flow_from_directory(directory = train_dir, target_size=image_size)
valdata   = vldata.flow_from_directory(directory = val_dir,   target_size=image_size)
#testdata  = tsdata.flow_from_directory(directory = test_dir,  target_size=image_size)
print(traindata.class_indices)

model = fit_model(traindata, valdata) 
model.summary()

model.save(save_model_path)


#predict picture
from predict_picture import ensemble_predictions
from keras.models import load_model
from dirtools import get_classes

img_path = 'test/40/005642.jpg_face.jpg'

members = [load_model('model')]         #write path
classes = get_classes(10) #CHECK testdata.class_indices!!!!

print(ensemble_predictions(members, img_path, classes))


#model_log
from model_log import ensemble_predictions
from predict_picture import get_real_predict
from predict_picture import ensemble_metrics
from predict_picture import plt_predict_real
from predict_picture import plt_age_error

from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
img_path = 'test/40/005642.jpg_face.jpg'
image_size = (256, 256)

members = [load_model('model')]     #write path

test_dir = 'test'
tsdata = ImageDataGenerator()
testdata  = tsdata.flow_from_directory(directory = test_dir,  target_size = image_size)

def get_key(dictionary, argument):
  for key, arg in dictionary.items():
    if arg == argument:
      return key
  return "ERROR"

classes = [int(get_key(testdata.class_indices, i)) for i in range(len(testdata.class_indices))]

print(ensemble_metrics(members, testdata))

real, predict = get_real_predict(members, classes, testdata.filepaths)

print('MAE:', mean_absolute_error(real, predict))
print('R2: ', r2_score(real, predict))

plt_age_error(members, classes, testdata.filepaths)

plt_predict_real(members, classes, testdata.filepaths)