from keras.models import load_model
import cv2
import numpy as np
import keras
import tensorflow as tf

train_ds = tf.keras.utils.image_dataset_from_directory(
  'imgs/trainimgs/',
  labels='inferred',
  label_mode='categorical',
  seed=123,
  color_mode="grayscale",
  image_size=(28, 28),
  batch_size=32)
labels = train_ds.class_names

model = load_model("currentmodel.h5")
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

def recognize_glyph(png):
    img = cv2.imread(png, 0)
    # img.show()
    # img.waitKey(0)
    img = np.array(img).reshape(-1, 28, 28, 1)
    probs = model.predict(img)
    problabels = probs.argmax(axis=-1)
    # print(labels)
    # print(labels[problabels[0]])
    return labels[problabels[0]]
