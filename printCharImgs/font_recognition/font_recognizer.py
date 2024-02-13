import glob
import os

import fitz
from fontTools.agl import toUnicode
from fontTools.ttLib import TTFont

import config
import text_action.analize
from cnn_model import *
from .pdf_reader import PDFReader
from . import pdf_reader as pr
from main import ROOT_DIR
from config import DefaultModel

# BAZA
fitz.TOOLS.set_subset_fontnames(True)


# BAZA


class FontRecognizer:
    # def __init__(self, *args, **kwargs):
    #     self.default_model_lang = None
    #     if 'model_folder_path' in kwargs:
    #         # self.model = Model(path=kwargs['model_path'], labels_path=kwargs['labels_path'])
    #         assert len(glob.glob(kwargs['model_folder_path'] + "/*")) == 2, "should be two files in folder: h5, json"
    #         self.model = Model(path=glob.glob(kwargs['model_folder_path'] + "/*.h5")[0],
    #                            labels_path=glob.glob(kwargs['model_folder_path'] + "/*.json")[0])
    #     elif 'model' in kwargs:
    #         assert type(kwargs['model']) is Model, "model is not cnn_model.Model type"
    #         self.model = kwargs['model']
    #     elif 'default_model' in kwargs:
    #         assert kwargs['default_model'] in config.default_models
    #         self.default_model_lang = kwargs['default_model']
    #         p = config.folders.get('default_models_folder')
    #         p = os.path.join(p, )
    #         # p = os.path.join(kwargs['default_model'], 'default_model')
    #         # self.model = Model(path=kwargs['default_model'])
    #     data_save_path = config.folders.get("extracted_data_folder")
    #     self.reader = PDFReader(data_save_path=data_save_path)
    #     self.text = None

    def __init__(self, model: Model):
        self.reader = PDFReader(config.folders.get("extracted_data_folder"))
        self.model = model
        self.default_model = None
        self.text = None

    @classmethod
    def load_default_model(cls, default_model: DefaultModel = DefaultModel.Russian_and_English):
        new_model = Model.load_default_model(default_model=default_model)
        new_model.default_model = default_model
        return cls(model=new_model)

    @classmethod
    def load_model(cls, path):
        assert len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) == 2, \
            "should be two files in folder: h5, json"
        # print(len([name for name in os.listdir(h5_and_json_folder) if os.path.isfile(name)]))
        # print(len([name for name in os.listdir(path) if os.path.isfile(name)]))
        new_model = Model.load_model_and_labels(model_path=glob.glob(path + "/*.h5")[0],
                                                model_labels_path=glob.glob(path + "/*.json")[0])
        return cls(new_model)

    # def __init__(self, model_path):
    #     if 'model_path' in kwargs:
    #         self.model = Model(path=kwargs['model_path'])
    #         data_save_path = config.folders.get("extracted_data_folder") if 'data_save_path' not in kwargs \
    #             else kwargs['data_save_path']
    #         self.reader = PDFReader(data_save_path=data_save_path)

    def restore_text(self, pdf_path, start_page=0, end_page=0):
        self.reader.read(pdf_path)
        self.text = self.__restore_text(pdf_path, self.__match_glyphs_and_encoding_for_all(), start=start_page,
                                        end=end_page)
        # print(self.text)
        if self.default_model is DefaultModel.Russian_and_English:
            # self.text = text_action.analize.correct_text(self.text)
            self.text = text_action.analize.correct_text_str(self.text)
        # print(self.text)
        return self.text

    def save_text(self, path):
        with open(path, "w") as f:
            f.write(self.text)

    def print_text(self):
        # return
        for i in self.text:
            print(i)

    def __restore_text(self, pdf_path, dictionary, start=0, end=0):
        doc = fitz.open(pdf_path)
        text = []
        text_str = ""
        if end == 0:
            end = doc.page_count
        pages = [doc[i] for i in range(start, end)]
        for page in pages:
            sentence = ""
            for blocks in page.get_text("dict", flags=95)['blocks']:
                try:
                    for lines in blocks['lines']:
                        line_text = ""
                        for spans in lines['spans']:
                            word = ""
                            # print(spans['text'])
                            if 'text' in spans:
                                d = spans['text'] = spans['text'].replace('\r', '')
                                w = 1
                            for index, char in enumerate(d):
                                # if char == '\r':
                                #     continue
                                # if char == '\t':
                                #     char = ' '
                                # print(char, spans['font'])
                                # print(spans['text'])
                                # Gonzalo
                                # сq}zz=q
                                try:
                                    if char in dictionary[spans['font']]:
                                        # print(char, dictionary[spans['font']][char], spans['font'], dictionary)
                                        word += dictionary[spans['font']][char]
                                    elif char in self.reader.white_spaces[spans['font'].split('.')[0]]:
                                        word += " "
                                    else:
                                        word += char
                                        # word += '□'
                                    # print(char, spans['font'])
                                except KeyError:
                                    # word += '*'
                                    word += char
                            line_text += word
                        line_text = line_text.lstrip(' ').rstrip(' ')
                        sentence += line_text
                        # print(sentence)
                        if line_text:
                            sentence += ' '
                        if len(sentence) >= 2 and sentence[-1] == "\n" and sentence[-2] == "\n":
                            continue
                        # if len(line_text) > 0 and line_text[-1] not in string.punctuation:
                        #     sentence += " "
                        #     continue

                        #ne nado
                        # sentence += '\n'

                        # if sentence[-1] in string.punctuation:
                        #     sentence += '\n'
                    # sentence += ' '
                    # sentence = sentence.strip()
                except KeyError:
                    pass
            # print("sentence", sentence)
            sentence = sentence.strip()
            # text.append(sentence)
            text_str += sentence
        return text_str

    def __match_glyphs_and_encoding_for_all(self):
        img_folders = self.reader.get_glyphs_path()
        # extracted_fonts_folder = os.path.join(ROOT_DIR, config.folders.get('extracted_data_folder'), "extracted_fonts")
        extracted_fonts_folder = config.folders.get("extracted_fonts_folder")
        # extracted_fonts_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), extracted_fonts_folder)
        # extracted_fonts_folder = os.path.join(ROOT_DIR, extracted_fonts_folder)
        fonts = glob.glob(extracted_fonts_folder + "/*")
        # print(fonts)
        dicts = {}
        for font_file in fonts:
            fontname = font_file.split('\\')[-1]
            ttf_font = TTFont(font_file)
            fitz_font = fitz.Font(fontfile=font_file)
            font_name_images = fontname.split('.')[0]
            # matching_res = self.__match_glyphs_and_encoding(ttf_font, fitz_font, img_folders + font_name_images)
            matching_res = self.__match_glyphs_and_encoding(ttf_font, fitz_font,
                                                            os.path.join(img_folders, font_name_images))
            # print(font_file, font_name_images)
            font_name_without_prefix = font_name_images.split('+')[1] if '+' in font_name_images else font_name_images
            dicts[font_name_images] = matching_res if font_name_without_prefix not in dicts else matching_res | \
                                                                                                       dicts[
                                                                                                           font_name_images.split(
                                                                                                               '+')[1]]
        # print(dicts)
        return dicts

    def __match_glyphs_and_encoding(self, ttf_font, fitz_font, images):

        images = glob.glob(images + "/*")
        dictionary = {}
        if 'cmap' in ttf_font:
            inv_cmap = {i: toUnicode(j) if 'uni' in j else j for i, j in
                        zip(ttf_font['cmap'].tables[0].cmap, ttf_font['cmap'].tables[0].cmap.values())}
        else:
            inv_cmap = {i: fitz_font.glyph_name_to_unicode(i) for i in ttf_font.getGlyphNames()}

        for img in images:
            key = ((img.split('\\')[-1]).split('.')[0]).split('_')[0]
            # print(key, type(key))
            # print(int(key))
            pred = self.model.recognize_glyph(img)
            # print(key)
            if key in inv_cmap:
                key = chr(inv_cmap[key])
            # print(key, chr(int(key)), pred, chr(int(pred)))
            # print(key, chr(key))
            # print(pred)
            dictionary[chr(int(key))] = chr(int(pred))
        # print(dictionary)
        return dictionary
