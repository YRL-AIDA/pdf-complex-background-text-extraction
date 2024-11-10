import config
from config import Language, DefaultModel
from model.model import Model
from pathlib import Path

# model = Model.create_default_model(default_model=DefaultModel.Russian_and_English)

model = Model()
rus_eng_dataset_folder = Path(config.folders.get('datasets-folder'), 'rus-eng')
model.train(dataset_path=rus_eng_dataset_folder, image_size=(28, 28), batch_size=2000, epochs=30)
model.save("my_model")
