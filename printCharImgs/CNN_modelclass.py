import configparser
import os

from keras.models import load_model
import cv2
import numpy as np
import ast

# try:
#     train_ds = tf.keras.utils.image_dataset_from_directory(
#       'imgs/trainimgs/',
#       labels='inferred',
#       label_mode='categorical',
#       seed=123,
#       color_mode="grayscale",
#       image_size=(28, 28),
#       batch_size=32)
#     labels = train_ds.class_names
# except BaseException:
#     pass
config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')
# rusenglabels = ast.literal_eval(config.get("LABELS", "labels"))
# englabels = ast.literal_eval(config.get("LABELS", "englabels"))
# ruslabels = ast.literal_eval(config.get("LABELS", "ruslabels"))
modelpathruseng = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model2.h5')
modelruseng = load_model(modelpathruseng)
modelruseng.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])


# def __init__(mode):
#     global model, labels
#     assert mode == 'Rus' or mode == 'Eng' or mode == 'RusEng', 'Wrong mode'
#     if mode == 'Rus':
#         model = load_model(modelpathrus)
#         labels = ast.literal_eval(config.get("LABELS", "ruslabels"))
#     elif mode == 'Eng':
#         model = load_model(modelpatheng)
#         labels = ast.literal_eval(config.get("LABELS", "englabels"))
#     elif mode == 'RusEng':
#         model = load_model(modelpathruseng)
#         labels = ast.literal_eval(config.get("LABELS", "rusenglabels"))
#
#
# def recognize_glyph(png, mode):
#     __init__(mode)
#     stream = open(png, "rb")
#     bytes = bytearray(stream.read())
#     numpyarray = np.asarray(bytes, dtype=np.uint8)
#     img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
#     img = np.array(img).reshape(-1, 28, 28, 1)
#     probs = model.predict(img, verbose=0)
#     problabels = probs.argmax(axis=-1)
#     return labels[problabels[0]]
#
#
# def __init__(mode):
#     print(mode)
#
# def qwer(mode):
#     __init__(mode)

class CNN:
    def __init__(self, mode):
        assert mode == 'Rus' or mode == 'Eng' or mode == 'RusEng', 'Wrong mode'
        if mode == 'Rus':
            self.model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Rus.h5'))
            self.labels = ast.literal_eval(config.get("LABELS", "ruslabels"))
        elif mode == 'Eng':
            self.model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Eng.h5'))
            self.labels = ast.literal_eval(config.get("LABELS", "englabels"))
        elif mode == 'RusEng':
            self.model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model2.h5'))
            self.labels = ast.literal_eval(config.get("LABELS", "rusenglabels"))

    def recognize_glyph(self, png):
        stream = open(png, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        img = np.array(img).reshape(-1, 28, 28, 1)
        probs = self.model.predict(img, verbose=0)
        problabels = probs.argmax(axis=-1)
        return self.labels[problabels[0]]