import os.path

import config
from cnn_model import Model
from font_recognition import *
from main import ROOT_DIR

model = Model()
# model.prepare_data()
# print(config.folders.get('images_folder') + "/output")
# model.train(epochs=100, data_path=config.folders.get('images_folder') + "/output", batch_size=10)
# model.train()
# model.save("rus_eng_no_reg_diff")
fr = FontRecognizer(model_folder_path="../data/models_and_classnames/rus_eng_no_reg_diff")
fr.restore_text(pdf_path="../data/pdf/1.pdf")
fr.print_text()
# model.train(data_path="../images/output")
# model.save("my_model")
# model.bb()

# print(ord('a'))
