from __future__ import division, print_function
from flask import Flask, render_template, request
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf

# Keras
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'model/Pests_Classification.h5'
#MODEL_PATH = 'model/Pests_NSC_V1.h5'
#MODEL_PATH = 'model/Pests_NSC_V2.h5'
#MODEL_PATH = 'model/Pests_NSC_V3.h5'
#model = load_model('modelPets.h5')
# Load your trained model
model = load_model(MODEL_PATH)
#print('Model loaded. check http://127.0.0.1:5000/')



def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(128, 128))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    # x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    x = x/255
    proba = model.predict(x.reshape(1, 128, 128, 3))
    # b=res[np.argmax(proba)]
    return proba


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        res =  ['Unknown', 'Bug shchitnik', 'Fall armyworm', 'Grasshopper', 'Jewel beetle', 'Mealy bug', 'Gryllotalpa', 'White grub' ]
        app.logger.info('%s',preds)
        app.logger.info('%s',preds[0,0])
        b = res[np.argmax(preds)]
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        # result = str(pred_class[0][0][1])               # Convert to string
        os.remove('./uploads/' + f.filename)
        return b
    return None


@app.route('/Pets')
def hlive():
    return 'ล้มเหลว'


@app.route('/index')
def myteam():
    # Main page
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
