# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""

"""
Структура dataset`a: 
    Изображения с именем вида: 000023.jpg_face.jpg
Должны быть файлы с метаданными.csv, структура: name,XX,age
"""
DATASET = 'appa-real-release'
trainmetafile = 'gt_avg_train.csv'
testnmetafile = 'gt_avg_test.csv'
validmetafile = 'gt_avg_valid.csv'

copy2_train_dir = 'train'
copy2_val_dir   = 'valid'
copy2_test_dir  = 'test'

#from zipfile import ZipFile
import shutil
import os
from dirtools import create_directory

def copy_images(file, source_dir, dest_dir):
    for line in file.readlines():
        imageinfo = line.split(',')  #name,XX,age,...
        apparent_age = round(float(imageinfo[2]))
        directory = apparent_age // 10
        directory *= 10
        shutil.copy2(os.path.join(source_dir, imageinfo[0] + '_face.jpg'), \
                    os.path.join(dest_dir, str(directory)))




#with ZipFile(DATASET_FILE + ".zip","r") as myzip:
    #myzip.extractall('DATASET')


# Каталог с набором данных
data_dir = 'DATASET'
#картинки
# Каталог с данными для обучения
train_dir = 'train'
# Каталог с данными для проверки
val_dir = 'valid'
# Каталог с данными для тестирования
test_dir = 'test'

classes = [str(i) for i in range(0, 91, 10)]
create_directory(train_dir, classes)
create_directory(val_dir, classes)
create_directory(test_dir, classes)


trainfile = open(trainmetafile, 'r')
testfile  = open(testnmetafile, 'r')
validfile = open(validmetafile, 'r')

for xfile in [trainfile, testfile, validfile]:
  imageinfo = xfile.readline().split(',')
  print(imageinfo)
  
#копирование изображений в папки
copy_images(trainfile, os.path.join(data_dir, train_dir), copy2_train_dir)
copy_images(validfile, os.path.join(data_dir, val_dir),   copy2_val_dir)
copy_images(testfile,  os.path.join(data_dir, test_dir),  copy2_test_dir)

#файлы прочитаны
trainfile.close()
testfile.close()
validfile.close()

