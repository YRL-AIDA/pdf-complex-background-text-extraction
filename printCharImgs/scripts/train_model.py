import config
from config import Language, DefaultModel
from cnn_model import Model

# model = Model.create_default_model(default_model=DefaultModel.Russian_and_English)

model = Model()
model.prepare_data_fontforge(char_pool=Language.Russian_and_English,
                             fonts_path="../data/fonts/fonts",
                             data_save_path="../data/datasets/123")
model.train(epochs=200)
model.save("custom_model")
