import config
from config import Language, DefaultModel
from cnn_model import Model


model = Model()
model.train(data_path="../data/datasets/123/output", epochs=1)
model.save("custom_model")

