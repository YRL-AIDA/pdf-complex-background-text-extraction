from pathlib import Path

from dataset_tools import data_prepare
import config

font_set_name = 'small_set'
fonts_folder = Path(config.folders.get('fonts_folders'), font_set_name)
data_prepare.create_dataset('rus-eng', fonts_folder, config.char_pool.get('rus_eng'))

