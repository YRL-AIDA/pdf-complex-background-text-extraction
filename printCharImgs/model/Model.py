import configparser
import os

from keras.models import load_model
import cv2
import numpy as np
import ast
import train, data_prepare
config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')

class Model:
    def __init__(self, *args, **kwargs):
        if 'path' in kwargs:
            self.weights= load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), config['CNN']['cnn_rus']))
        elif

    def prepare_data(self, fonts_path, language='RusEng'):
        data_prepare.prepdata(fonts_path,language)

    def train(self):
        train.train(self.name)

    def recognize_glyph(self, png):
        stream = open(png, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        img = np.array(img).reshape(-1, 28, 28, 1)
        probs = self.model.predict(img, verbose=0)
        problabels = probs.argmax(axis=-1)
        return self.labels[problabels[0]]
