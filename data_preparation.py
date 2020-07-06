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
import shutil
import os
from zipfile import ZipFile
from dirtools import create_directory
from dirtools import get_agedir
from dirtools import get_classes

def copy_images(path_metafile, source_dir, dest_dir, classes):
    file = open(path_metafile, 'r')
    file.readline()
    for line in file.readlines():
        imageinfo = line.split(',')  #name,XX,age,...
        apparent_age = round(float(imageinfo[2]))
        if apparent_age >= 0 and apparent_age <= 99:
            directory = get_agedir(apparent_age, classes)
            shutil.copy2(os.path.join(source_dir, imageinfo[0] + '_face.jpg'), \
                    os.path.join(dest_dir, str(directory)))
    file.close()
    
def prepare_zip_data(period = 1, path_zip_data = 'appa-real-release.zip', \
                 sorted_data_locate = ['train', 'valid', 'test'], \
                 prepare_data_dirs  = ['appa-real-release/train', \
                                       'appa-real-release/valid', \
                                       'appa-real-release/test'], \
                metadata_files = ['appa-real-release/gt_avg_train.csv', \
                                   'appa-real-release/gt_avg_valid.csv', \
                                   'appa-real-release/gt_avg_test.csv'], \
                 not_sorted_data_locate = None):
    
    if len(metadata_files) != len(sorted_data_locate) != len(prepare_data_dirs):
        return 'ERROR: len(metadata_files) != len(sorted_data_locate) != len(prepare_data_dirs)'
    
    if not_sorted_data_locate == None:
      not_sorted_data_locate = 'data_not_sorted_workfile_will_be_deleted'
    
    #classes = get_classes(period)
    with ZipFile(path_zip_data, "r") as myzip:
        myzip.extractall(not_sorted_data_locate)
    
    for i in range(len(sorted_data_locate)):
        meta   = os.path.join(not_sorted_data_locate,     metadata_files[i])
        source = os.path.join(not_sorted_data_locate,  prepare_data_dirs[i])
        dest   = sorted_data_locate[i]      
        prepare_age_data(period, meta, source, dest)
    
    if os.path.exists('data_not_sorted_workfile_will_be_deleted'):
        shutil.rmtree('data_not_sorted_workfile_will_be_deleted')
    
    # Каталог с набором данных
    #data_dir = not_sorted_data_locate
    #картинки
    # Каталог с данными для обучения
    #train_dir = 'train'
    # Каталог с данными для проверки
    #val_dir = 'valid'
    # Каталог с данными для тестирования
    #test_dir = 'test'
    
    #trainmetafile = 'gt_avg_train.csv'
    #testnmetafile = 'gt_avg_test.csv'
    #validmetafile = 'gt_avg_valid.csv'
#    
#    copy2_train_dir = sorted_data_locate[0]
#    copy2_val_dir   = sorted_data_locate[1]
#    copy2_test_dir  = sorted_data_locate[2]
#    
#    create_directory(copy2_train_dir, classes)
#    create_directory(copy2_val_dir, classes)
#    create_directory(copy2_test_dir, classes)
#    
#    trainfile = open(trainmetafile, 'r')
#    testfile  = open(testnmetafile, 'r')
#    validfile = open(validmetafile, 'r')
#    
#    for xfile in [trainfile, testfile, validfile]:
#      imageinfo = xfile.readline().split(',')
#      print(imageinfo)
      
    #копирование изображений в папки
#    copy_images(trainfile, os.path.join(data_dir, train_dir), copy2_train_dir, classes)
#    copy_images(validfile, os.path.join(data_dir, val_dir),   copy2_val_dir,   classes)
#    copy_images(testfile,  os.path.join(data_dir, test_dir),  copy2_test_dir,  classes)
    
    #файлы прочитаны
#    trainfile.close()
#    testfile.close()
#    validfile.close()

def prepare_age_data(period, path_metafile, source_dir, dest_dir = 'sorted_data'):
    classes = get_classes(period)
    create_directory(dest_dir, classes)
    copy_images(path_metafile, source_dir, dest_dir, classes)