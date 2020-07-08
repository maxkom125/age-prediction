# -*- coding: utf-8 -*-
"""
Created Jun 7 2020

@author: Maksym Komarov
"""
#from keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt
from predict_picture import ensemble_predictions

#def ensemble_predictions(members, img_path, classes, show_image = True, image_size = (256, 256)):
#	img = image.load_img(img_path, target_size=image_size)
#	testim = image.img_to_array(img)
#	testim = np.expand_dims(testim, axis=0)
#	# Предсказания
#	yhats = [model.predict(testim)[0] for model in members]
#	yhats = np.array(yhats)
#	#summed = np.sum(yhats, axis=0) / len(members)
#	# argmax - наиболее вероятный возраст
#	#result = np.argmax(summed, axis=1)
#	#result = get_key(traindata.class_indices, result)
#	#classes = [int(get_key(traindata.class_indices, i)) for i in range(len(yhats[0]))]
#	classes = np.array(classes, dtype = int)
#	ans = 0
#	#Матожидание
#    #Итоговое значение - среднее по всем элементам ансамбля
#	for yhat in yhats:
#		result = np.multiply(yhat, classes)
#		result = np.sum(result)
#		#print(result)
#		ans += result
#	ans /= len(members)
#	if show_image:
#            #print(yhats) вероятности
#            plt.imshow(img)
#            plt.show()
#	return np.round(ans, decimals = 2)

def get_real_predict(members, classes, datapaths, sort = False): #Two arrays
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
        predict.append(ensemble_predictions(members, path, classes, False))
        real.append(int(str_real))
    else:
        predict[int(str_real)].append(ensemble_predictions(members, path, classes, False))
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
def plt_predict_real(members, classes, datapaths):
#  real_predict = dict(zip(get_real_predict(members, classes, datapaths)))
#  real_predict = sorted(real_predict.items(), key=operator.itemgetter(2))
  real, predict = get_real_predict(members, classes, datapaths, sort = True)
  plt.figure(figsize=(50, 35))
  plt.plot(predict, 'bo') 
  plt.legend('predict age')
  plt.plot(real, 'go')
  plt.legend('real age')
  plt.ylabel('Age')
  plt.xlabel('number')
  plt.show()
  return

def plt_age_error(members, classes, datapaths):
  real, predict = get_real_predict(members, classes, datapaths)
  real    = np.array(real)
  predict = np.array(predict)
  #plt.figure(figsize=(50, 35))
  plt.plot(real, np.subtract(predict, real), 'ro') 
  plt.ylabel('Absolute error')
  plt.xlabel('Age')
  plt.show()
  return




