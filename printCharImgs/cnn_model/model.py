import glob
import os.path
import shutil

import cv2
import numpy as np
from keras.models import load_model
import tensorflow as tf

import config
from config import Language, DefaultModel
import main
from .trainer import Trainer
from . import data_prepare
from main import ROOT_DIR
import json


class Model:
    # def __init__(self, **kwargs):
    #     """
    #     @path and @dataset in case have prepared h5 and dataset, @default_model rus|eng|rus+eng
    #     """
    #     assert 'path' and 'labels_path' in kwargs or \
    #            ('default_model' in kwargs and kwargs['default_model'] in config.default_models) or len(kwargs) == 0
    #     if 'path' and 'labels_path' in kwargs:
    #         self.weights = load_model(kwargs['path'])
    #         with open(kwargs['labels_path'], 'r') as j:
    #             self.labels = json.loads(j.read())
    #     elif 'default_model' in kwargs:
    #         m_name = config.default_models_and_labels[kwargs['default_model']]['model_name']
    #         self.labels = config.default_models_and_labels[kwargs['default_model']]['labels']
    #         self.weights = load_model(os.path.join(config.folders['default_models_folder'], m_name))
    #     self.data_path = None
    #     self.trainer = Trainer()

    def __init__(self):
        self.weights = None
        self.labels = None
        self.data_path = None
        self.trainer = Trainer()
        self.logs_path = None

    def __del__(self):
        if self.logs_path is None:
            return
        if os.path.exists(self.logs_path):
            shutil.rmtree(self.logs_path)

    @classmethod
    def load_default_model(cls, default_model: DefaultModel = DefaultModel.Russian_and_English):
        print(default_model)
        new_model = cls()
        new_model.weights = default_model.Russian_and_English.value['model']
        new_model.labels = default_model.Russian_and_English.value['labels']
        # print(new_model.weights.layers[-1].output_shape)
        new_model.__assert_labels_and_model()
        return new_model

    @classmethod
    def load_model_and_labels(cls, model_path, model_labels_path):
        assert model_path.split('/')[-1].split('\\')[-1].split('.')[-1] == 'h5'
        assert model_labels_path.split('/')[-1].split('\\')[-1].split('.')[-1] == 'json'
        new_model = cls()
        new_model.weights = load_model(model_path)
        with open(model_labels_path, 'r') as j:
            new_model.labels = json.loads(j.read())
        new_model.__assert_labels_and_model()
        return new_model

    @classmethod
    def load_by_h5_and_json_folder(cls, h5_and_json_folder):
        print(len([name for name in os.listdir(h5_and_json_folder) if os.path.isfile(name)]))
        assert len(glob.glob(os.path.join(h5_and_json_folder, "*"))) == 2
        h5_path = glob.glob(os.path.join(h5_and_json_folder, "*.h5"))[0]
        json_path = glob.glob(os.path.join(h5_and_json_folder, "*.json"))[0]
        cls.load_model_and_labels(h5_path, json_path)

    def __assert_labels_and_model(self):
        assert self.weights.layers[-1].output_shape[-1] == len(self.labels)

    def prepare_data(self, fonts_path=config.folders.get('fonts_folder'),
                     data_save_path=config.folders.get("images_folder"),
                     char_pool: config.Language = config.Language.Russian_and_English or list):
        if type(char_pool) is config.Language:
            char_pool = char_pool.value
        assert os.path.exists(fonts_path), "no folder with fonts"
        self.data_path = data_save_path + "/output"
        data_prepare.prepdata(fonts_path, data_save_path, char_pool)

    def train(self, data_path=None, image_size: tuple = (28, 28), batch_size=2000, epochs=100,
              logs_path=os.path.join(ROOT_DIR, "data", "logs")):
        """
        if no data_path, last prepared_data for model will be used
        """
        if data_path is None:
            if self.data_path is not None:
                data_path = self.data_path
            else:
                # data_path = os.path.join(main.ROOT_DIR, config.folders.get("images_folder"), "output")
                data_path = config.folders.get('output_train')
        assert data_path is not None, "No data for train"
        assert len(next(os.walk(data_path))[1]) == 4, "should be 4 folders: train, val, test, test_from_train"

        if os.path.exists(logs_path):
            shutil.rmtree(logs_path)
        os.makedirs(logs_path)

        self.weights, self.labels = self.trainer.train(data_path, image_size, batch_size, epochs, logs_path)
        print(self.weights.layers[-1].output_shape)

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
        # p = os.path.join(ROOT_DIR, config.folders.get('custom_models_folder'), name)
        p = os.path.join(config.folders.get('custom_models_folder'), name)
        if os.path.exists(p):
            shutil.rmtree(p)
        os.makedirs(p)
        files_path = os.path.join(p, name)
        self.weights.save(files_path + ".h5")
        with open(files_path + ".json", 'w') as f:
            json.dump(self.labels, f)

        logs = os.listdir(self.logs_path)
        for log in logs:
            shutil.move(os.path.join(self.logs_path, log), os.path.join(p, "logs"))
