import os.path

import config
from cnn_model import Model
from font_recognition import *
from main import ROOT_DIR

model = Model()
model.prepare_data_fontforge()
model.train()
model.save("rus_eng")
fr = FontRecognizer.load_model(path="../data/models_and_classnames/rus_eng_no_reg_diff")
fr.restore_text(pdf_path="../data/pdf/1.pdf")
fr.print_text()

