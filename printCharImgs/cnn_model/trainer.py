import tensorflow as tf
from pathlib import Path
import os
from tensorflow import keras
from keras import layers


class Trainer:
    def __init__(self):
        self.w = None
        self.h = None
        self.batch_size = None
        self.seq_model = None
        self.epochs = None
        self.path = None
        self.num_classes = None

    def train(self, data_path, image_size, batch_size, epochs):
        assert os.path.exists(data_path)
        self.__init__()
        self.w, self.h = image_size
        self.path = data_path
        p = Path(self.path)
        self.num_classes = len(next(os.walk(next(p.glob('*'))))[1])
        self.batch_size = batch_size
        train_ds, validation_ds, test_ds, test_from_train_ds = self.__create_datasets()
        if self.seq_model is None:
            self.set_model()
        self.seq_model.summary()
        self.seq_model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        self.seq_model.fit(train_ds, validation_data=validation_ds, batch_size=batch_size, epochs=epochs)
        # labels = [int(i) for i in train_ds.class_names]
        labels = train_ds.class_names
        return self.seq_model, labels

    def __create_datasets(self):
        image_size = (self.w, self.h)
        b_size = self.batch_size
        # b_size = 32
        train_ds = tf.keras.utils.image_dataset_from_directory(
            self.path + "/train",
            labels='inferred',
            label_mode='categorical',
            seed=33,
            color_mode="grayscale",
            image_size=image_size,
            batch_size=b_size)
        validation_ds = tf.keras.utils.image_dataset_from_directory(
            self.path + "/val",
            labels='inferred',
            label_mode='categorical',
            seed=33,
            color_mode="grayscale",
            image_size=image_size,
            batch_size=b_size)
        test_ds = tf.keras.utils.image_dataset_from_directory(
            self.path + "/test",
            labels='inferred',
            label_mode='categorical',
            seed=33,
            color_mode="grayscale",
            image_size=image_size,
            batch_size=b_size)
        test_from_train_ds = tf.keras.utils.image_dataset_from_directory(
            self.path + "/test_from_train",
            labels='inferred',
            label_mode='categorical',
            seed=33,
            color_mode="grayscale",
            image_size=image_size,
            batch_size=b_size)
        return train_ds, validation_ds, test_ds, test_from_train_ds

    def set_model(self, model: tf.keras.Model = None):
        input_shape = (self.w, self.h, 1)
        if model is None:
            self.seq_model = keras.Sequential(
                [
                    keras.Input(shape=input_shape),
                    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                    layers.MaxPooling2D(pool_size=(2, 2)),
                    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                    layers.MaxPooling2D(pool_size=(2, 2)),
                    layers.Flatten(),
                    layers.Dropout(0.2),
                    layers.Dense(256, activation="relu"),
                    layers.Dropout(0.5),
                    layers.Dense(self.num_classes, activation="softmax"),
                ]
            )
        else:
            self.seq_model = model

