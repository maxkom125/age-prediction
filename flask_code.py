# CODE NEEDS IMPROVEMENT
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 2020

@author: Maksym Komarov
"""    
from flask import request, Flask, jsonify
from class_agepredictor import AgePredictor
from class_faceimage import FaceImage

app = Flask(__name__)      

@app.route('/', methods=['POST'])
def home_page(): 
    if request.method == 'POST':
        ServerAgePredictor = AgePredictor('E:/Maksym/GitHub/age-prediction/modelFINAL0') # Bad place to create
        data = request.form.to_dict()
        images = []
        names = []
        
        for i in range(len(data)):
            dataitem = data.popitem()
            img = dataitem[1]
            name = dataitem[0]
            img = bytes(img, encoding = 'utf-8')
            images.append(img)
            names.append(name)
            
        local_history = []
        i = 0
        for i in range(len(images) - 1, -1, -1):
            age = ServerAgePredictor.predict(FaceImage(images[i]))
            age = str(age)
            local_history.append((names[i], age))
            i += 1
        
        return jsonify(dict(local_history))
        
if __name__ == '__main__':
    app.run() #debug = True
    
    
    
