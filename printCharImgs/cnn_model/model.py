import glob
import os.path
import shutil

import cv2
import numpy as np
from keras.models import load_model
import tensorflow as tf

import config
import main
from .trainer import Trainer
from . import data_prepare
from main import ROOT_DIR
import json


class Model:
    def __init__(self, **kwargs):
        """
        @path and @dataset in case have prepared h5 and dataset, @default_model rus|eng|rus+eng
        """
        assert 'path' and 'labels_path' in kwargs or \
               ('default_model' in kwargs and kwargs['default_model'] in config.default_models) or len(kwargs) == 0
        if 'path' and 'labels_path' in kwargs:
            self.weights = load_model(kwargs['path'])
            with open(kwargs['labels_path'], 'r') as j:
                self.labels = json.loads(j.read())
        elif 'default_model' in kwargs:
            self.weights = load_model("models/" + kwargs['default_model'] + ".h5")
            self.labels = config.labels.get(kwargs['default_model'])

        self.data_path = None
        self.trainer = Trainer()

    def prepare_data(self, fonts_path=config.folders.get('fonts_folder'),
                     data_save_path=config.folders.get("images_folder"),
                     char_pool_name='rus_eng_no_reg_diff'):
        fonts_path = os.path.join("../", fonts_path)
        data_save_path = os.path.join("../", data_save_path)
        assert os.path.exists(fonts_path), "no folder with fonts"
        assert char_pool_name in config.char_pool.keys(), "no such language, check config.py char_pool"
        self.data_path = data_save_path + "/output"
        data_prepare.prepdata(fonts_path, data_save_path, config.char_pool.get(char_pool_name))

    def train(self, data_path=None, image_size: tuple = (28, 28), batch_size=2000, epochs=100):
        """
        if no data_path, last prepared_data for model will be used
        """
        if data_path is None:
            if self.data_path is not None:
                data_path = self.data_path
            else:
                data_path = os.path.join(main.ROOT_DIR, config.folders.get("images_folder"), "output")
        assert data_path is not None, "No data for train"
        assert len(next(os.walk(data_path))[1]) == 4, "should be 4 folders: train, val, test, test_from_train"
        self.weights, self.labels = self.trainer.train(data_path, image_size, batch_size, epochs)

    def set_model(self, model: tf.keras.Model):
        self.trainer.set_model(model)

    def recognize_glyph(self, png):
        stream = open(png, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        img = np.array(img).reshape(-1, 28, 28, 1)
        probs = self.weights.predict(img, verbose=0)
        problabels = probs.argmax(axis=-1)
        return self.labels[problabels[0]]

    def bb(self):
        png = "D:\\rep\\fonts-recognition\\printCharImgs\\images\\output\\test\\8\\8_259.png"
        stream = open(png, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        img = np.array(img).reshape(-1, 28, 28, 1)
        probs = self.weights.predict(img, verbose=0)
        problabels = probs.argmax(axis=-1)
        return self.labels[problabels[0]]

    def save(self, name):
        assert self.weights is not None, "no trained model to save"
        p = os.path.join(ROOT_DIR, config.folders.get('custom_models_folder'), name)
        if os.path.exists(p):
            shutil.rmtree(p)
        os.makedirs(p)
        files_path = os.path.join(p, name)
        self.weights.save(files_path + ".h5")
        with open(files_path + ".json", 'w') as f:
            json.dump(self.labels, f)

