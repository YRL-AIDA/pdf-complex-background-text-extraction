from pathlib import Path

from dataset_tools import data_prepare
import config

font_set_name = 'fonts'
fonts_folder = Path(config.folders.get('fonts_folders'), font_set_name)
data_prepare.create_dataset('rus-eng', fonts_folder, config.char_pool.get('rus_eng'))
data_prepare.create_dataset('eng', fonts_folder, config.char_pool.get('eng'))
data_prepare.create_dataset('rus', fonts_folder, config.char_pool.get('rus'))
