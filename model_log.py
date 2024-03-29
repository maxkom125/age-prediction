# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
#from keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt
from predict_picture import ensemble_predictions
def _get_real_predict(members, datapaths, sort = False): #Two arrays
  predict = []
  real = []
  if sort == True:
      predict = [[] for i in range(100)]
      real    = [[] for i in range(100)]
      
  for path in datapaths:
    #path вида 'train/23/001297.jpg_face.jpg'
    class_name_start = path.find('/') + 1
    class_name_end = path.find('/', class_name_start) - 1
    str_real = path[class_name_start: class_name_end + 1]    
    if sort == False:
        predict.append(ensemble_predictions(members, path, False))
        real.append(int(str_real))
    else:
        predict[int(str_real)].append(ensemble_predictions(members, path, False))
        real[int(str_real)].append(int(str_real))
        
  if sort != False:
      if sort == 'Reverse':
          reverse = True
      else:
          reverse = False
      for i in range(len(predict)):
          predict[i] = sorted(predict[i], reverse = reverse)
      anspr = []
      ansreal = []
      for i in range(len(predict)):
          anspr += predict[i]
          ansreal += real[i]
      real = ansreal
      predict = anspr
  return real, predict

def ensemble_metrics(members, testdata):
  scores = [model.evaluate(testdata) for model in members]
  ans = ''
  for i in range(len(scores[0])): #по каждой метрике
    metric = 0
    for m in range(len(members)):  #по каждой сети ансамбля   
      metric += scores[m][i]
    metric = round(metric / len(members), 3)
    ans += members[0].metrics_names[i]+ ': ' + str(metric) + ';  '
  ans = ans[:-3]
  return ans

#import operator
def plt_predict_real(members, datapaths):
  real, predict = _get_real_predict(members, datapaths, sort = True)
  plt.figure(figsize=(50, 35))
  plt.plot(predict, 'bo') 
  plt.legend('predict age')
  plt.plot(real, 'go')
  plt.legend('real age')
  plt.ylabel('Age')
  plt.xlabel('number')
  plt.show()
  return

def plt_age_error(members, datapaths):
  real, predict = _get_real_predict(members, datapaths)
  real    = np.array(real)
  predict = np.array(predict)
  #plt.figure(figsize=(50, 35))
  plt.plot(real, np.subtract(predict, real), 'ro') 
  plt.ylabel('Absolute error')
  plt.xlabel('Age')
  plt.show()
  return

def history(agepredictor):
    i = 0
    for history in agepredictor.history:
        if history == None:
            print('model ' + str(i) + ' history is empty')
        else:
            print(history.history.keys())
            # summarize history for accuracy
            plt.plot(history.history['accuracy'])
            plt.plot(history.history['val_accuracy'])
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            plt.show()
            # summarize history for loss
            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            plt.show()
        i += 1
    return




