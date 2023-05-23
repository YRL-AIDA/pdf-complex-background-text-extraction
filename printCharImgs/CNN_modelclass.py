import os

from keras.models import load_model
import cv2
import numpy as np

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
noregdiflabels = ['!', '#', '$', '%', '&', "'", '(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ';', '=', '@', 'Rus_a', 'Rus_b', 'Rus_ce', 'Rus_ch', 'Rus_d', 'Rus_e', 'Rus_f', 'Rus_g', 'Rus_h', 'Rus_hard', 'Rus_i', 'Rus_ib', 'Rus_k', 'Rus_l', 'Rus_m', 'Rus_n', 'Rus_o', 'Rus_p', 'Rus_r', 'Rus_s', 'Rus_sh', 'Rus_sha', 'Rus_soft', 'Rus_t', 'Rus_th', 'Rus_u', 'Rus_uh', 'Rus_v', 'Rus_ya', 'Rus_yu', 'Rus_z', 'Rus_zh', '[', ']', '^', '_', '`', 'a', 'asterisk', 'b', 'backslash', 'c', 'colon', 'copyright', 'd', 'dot', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'less', 'm', 'more', 'n', 'o', 'p', 'q', 'question', 'quotedbl', 'r', 's', 'slash', 't', 'tm', 'u', 'v', 'vertical', 'w', 'x', 'y', 'z', '{', '}', '~']
labels = noregdiflabels
# model = load_model("currentmodel.h5")
# model = load_model("curcur.h5")
# model = load_model("penaug.h5")
modelpath = config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curcur.h5')
model = load_model(modelpath)
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
print(labels)
def recognize_glyph(png):
    img = cv2.imread(png, 0)
    # img.show()
    # img.waitKey(0)
    img = np.array(img).reshape(-1, 28, 28, 1)
    probs = model.predict(img, verbose=0)
    problabels = probs.argmax(axis=-1)
    # print(labels)
    # print(labels[problabels[0]])
    return labels[problabels[0]]
