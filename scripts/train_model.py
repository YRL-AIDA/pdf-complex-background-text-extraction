import config
from model.model import Model
from pathlib import Path

model = Model()
rus_eng_dataset_folder = Path(config.folders.get('datasets_folder'), 'rus-eng')
model.train(dataset_path=rus_eng_dataset_folder, image_size=(28, 28), batch_size=128, epochs=30)
model.save("rus_eng")

model = Model()
eng_dataset_folder = Path(config.folders.get('datasets_folder'), 'eng')
model.train(dataset_path=eng_dataset_folder, image_size=(28, 28), batch_size=128, epochs=30)
model.save("eng")

model = Model()
rus_dataset_folder = Path(config.folders.get('datasets_folder'), 'rus')
model.train(dataset_path=rus_dataset_folder, image_size=(28, 28), batch_size=128, epochs=30)
model.save("rus")
