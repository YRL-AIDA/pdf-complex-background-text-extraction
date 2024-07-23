import ast
import os
import shutil
import subprocess
import warnings
from pathlib import Path
import config
from icecream import ic

import splitfolders

from utils import functions


def create_dataset(dataset_name: str, fonts_path: Path, char_pool: list):
    assert dataset_name != 'last_prepared', 'занято'

    dataset_save_path = Path(config.folders.get('datasets_folder'), dataset_name)
    ic(dataset_save_path, fonts_path)
    print(char_pool)

    if dataset_save_path.exists():
        shutil.rmtree(dataset_save_path)

    os.makedirs(dataset_save_path)

    images_path = Path(dataset_save_path, 'images')

    __extract_glyphs(images_path, fonts_path, char_pool)

    splitfolders.ratio(images_path, output=dataset_save_path, ratio=(0.7, 0.2, 0.1), move=False)
    last_prepared = config.folders.get("last_prepared_data")

    if os.path.exists(last_prepared):
        shutil.rmtree(last_prepared)

    shutil.rmtree(images_path)
    print("last prepared copying")
    shutil.copytree(dataset_save_path, last_prepared)


def __extract_glyphs(images_save_path: Path, fonts_path: Path, char_pool: list):

    uni_char_pool = [str(ord(char)) for char in char_pool]
    for char in char_pool:
        os.makedirs(Path(images_save_path, str(ord(char))))

    counter = 0
    # font_files = os.listdir(fonts_path)
    font_files = list(fonts_path.iterdir())
    warnings.filterwarnings("ignore", category=Warning)
    for font_file in font_files:
        font_name = os.fsdecode(font_file)
        font_file_path = fr'"{fonts_path}/{font_file}"'
        try:
            DEVNULL = open(os.devnull, 'wb')
            result = subprocess.check_output(f"ffpython ../ffwrapper/fontforge_wrapper.py True {images_save_path} {font_file_path} {counter} {' '.join(uni_char_pool)}", stderr=DEVNULL)
        except:
            continue
        result = result.decode('utf-8')
        result = ast.literal_eval(result)
        for img in result:
            functions.correctly_resize(img)
        counter += 1

