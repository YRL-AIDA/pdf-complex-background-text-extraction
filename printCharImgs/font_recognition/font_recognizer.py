import glob
import os
import re
import warnings
from typing import Any, Iterable

import PyPDF2
import cv2
import fitz
import numpy as np
from fontTools.agl import toUnicode
from fontTools.ttLib import TTFont
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTChar, LTPage, LTTextBox, LTTextBoxHorizontal, LTTextBoxVertical
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral
from pdfminer.high_level import extract_text, extract_pages
from io import StringIO

import config
import text_action.analize
from cnn_model import *
from config import DefaultModel
from src.utils import junkstring
from text_action import analize
from .pdf_reader import PDFReader

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
        self.match_dict = {}
        self.cached_fonts = None
        self.fontname2basefont = {}
        self.unicodemaps = {}

    @classmethod
    def load_default_model(cls, default_model: DefaultModel = DefaultModel.Russian_and_English):
        new_model = Model.load_default_model(default_model=default_model)
        new_model.default_model = default_model
        recognizer = cls(model=new_model)
        recognizer.default_model = default_model
        return recognizer

    # def __set_default_model
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
        Exception("no use")
        self.text = None
        self.match_dict = {}
        self.reader.read(pdf_path)
        fonts_match_dict = self.__match_glyphs_and_encoding_for_all
        # self.text = self.__restore_text(pdf_path, fonts_match_dict, start=start_page, end=end_page)
        self.text = self.__restore_text(pdf_path, fonts_match_dict, start=start_page, end=end_page)
        # self.text
        # print(self.text)
        if self.default_model is DefaultModel.Russian_and_English:
            # self.text = text_action.analize.correct_text(self.text)
            self.text = text_action.analize.correct_text_str(self.text)
        return self.text

    def restore_text_fontforge(self, pdf_path, start_page=0, end_page=0):
        assert end_page > start_page or start_page == end_page == 0, "wrong pages range"
        self.text = ''
        self.match_dict = {}
        self.reader.read(pdf_path)
        # self.match_dict = self.reader.white_spaces
        warnings.warn('self.match_dict = self.reader.white_spaces ????')
        warnings.warn('right now ignoring #.superior')
        self.__match_glyphs_and_encoding_for_all_fontforge
        fonts_match_dict = self.match_dict
        self.text = self.__restore_text2(pdf_path, fonts_match_dict, start=start_page, end=end_page)
        self.text = re.sub(r'\s+', ' ', self.text)
        if self.default_model is DefaultModel.Russian_and_English:
            # self.text = text_action.analize.correct_text(self.text)
            self.text = text_action.analize.correct_text2(self.text)
        # self.text = analize.t9_text(self.text)
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
                            if 'text' not in spans:
                                continue
                            # binary = f'{spans["text"]}'.encode('utf-8')
                            d = spans['text'] = spans['text'].replace('\r', '')
                            w = spans['font']
                            print(d)
                            for index, char in enumerate(d):
                                if char in ['\t', ' ']:
                                    word += ' '
                                    continue
                                try:
                                    if char in dictionary[spans['font']]:
                                        word += dictionary[spans['font']][char]
                                        # word += "*"
                                    elif char in self.reader.white_spaces[spans['font'].split('.')[0]]:
                                        word += " "
                                    else:
                                        # word += char
                                        word += '□'
                                    # print(char, spans['font'])
                                except KeyError:
                                    word += '*'
                                    # word += char
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

    def __restore_text2(self, pdf_path, dictionary, start=0, end=0):
        fulltext = ''
        # Open the PDF file
        self.cached_fonts = None
        self.fontname2basefont = {}
        self.unicodemaps = {}
        with open(pdf_path, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            pages_count = resolve1(document.catalog['Pages'])['Count']
            end = pages_count if end == 0 else end
            # pdf_reader.py = PyPDF2.PdfFileReader(fp)
            # pages_count = pdf_reader.py.numPages

            rsrcmgr = PDFResourceManager()
            laparams = LAParams()

            # Create a PDF device object
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # Iterate through each page of the PDF
            for page_num, page in enumerate(PDFPage.create_pages(document)):

                if page_num < start:
                    continue
                elif page_num >= end:
                    break
                interpreter.process_page(page)
                layout = device.get_result()
                cached_fonts = {}
                fonts = page.resources.get('Font')
                if not isinstance(fonts, dict):
                    Exception('fonts should be dictionary, ti nepravilno napisal kod(')
                for font_key, font_obj in fonts.items():
                    font_dict = resolve1(font_obj)
                    encoding = resolve1(font_dict['Encoding'])
                    f = rsrcmgr.get_font(objid=font_obj.objid, spec={'name': resolve1(font_obj)['BaseFont'].name})
                    self.fontname2basefont[f.fontname] = f.basefont if hasattr(f, 'basefont') else f.fontname

                    if hasattr(f, 'unicode_map') and hasattr(f.unicode_map, 'cid2unichr'):
                        basefont_else_fontname = self.fontname2basefont[f.fontname]
                        self.unicodemaps[basefont_else_fontname] = f.unicode_map.cid2unichr
                    if not (isinstance(encoding, dict) and ('/Differences' in encoding or 'Differences' in encoding)):
                        cached_fonts[f.fontname] = []
                        continue
                    # char_set_arr1 = f.descriptor['CharSet'].decode('utf-8').split('/')
                    char_set_arr = [q.name if isinstance(q, PSLiteral) else '' for q in encoding['Differences']]
                    # char_set_arr = [encoding['Differences']]
                    # ВЕСIНИк В0ССIАН0ВИIЕЛЬН0Й МСIИЦИИ 0вществеwwому цеwтру <Сулевwо-прqвовqя pegopmq+ 10 лет *ЖGМНДСР УNSквFЧС &FFP
                    cached_fonts[f.fontname] = char_set_arr
                self.cached_fonts = rsrcmgr._cached_fonts
                self.walk(layout, cached_fonts, fulltext)

        self.text = analize.remove_hyphenations(self.text)
        return self.text

    @property
    def __match_glyphs_and_encoding_for_all(self):
        img_folders = self.reader.get_glyphs_path()
        print("glyphpath", self.reader.get_glyphs_path())
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
            font_name_images = font_name_images.split(junkstring)[0]
            print("fontnameimgs", font_name_images)
            # matching_res = self.__match_glyphs_and_encoding(ttf_font, fitz_font, img_folders + font_name_images)
            matching_res = self.__match_glyphs_and_encoding(ttf_font, fitz_font,
                                                            os.path.join(img_folders, font_name_images))
            # print(font_file, font_name_images)
            font_name_without_prefix = font_name_images.split('+')[1] if '+' in font_name_images else font_name_images
            dicts[font_name_images] = matching_res if font_name_without_prefix not in dicts else matching_res | \
                                                                                                       dicts[
                                                                                                           font_name_images.split(
                                                                                                               '+')[1]]
        print(dicts)
        return dicts
    @property
    def __match_glyphs_and_encoding_for_all_fontforge(self):
        img_folders = self.reader.get_glyphs_path()
        print("glyphpath", self.reader.get_glyphs_path())
        # extracted_fonts_folder = os.path.join(ROOT_DIR, config.folders.get('extracted_data_folder'), "extracted_fonts")
        extracted_fonts_folder = config.folders.get("extracted_fonts_folder")
        # extracted_fonts_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), extracted_fonts_folder)
        # extracted_fonts_folder = os.path.join(ROOT_DIR, extracted_fonts_folder)
        fonts = glob.glob(extracted_fonts_folder + "/*")
        # print(fonts)
        dicts = {}
        for font_file in fonts:
            fontname = font_file.split('\\')[-1]
            font_name_images = fontname.split('.')[0]
            font_name_images = font_name_images.split(junkstring)[0]
            print("fontnameimgs", font_name_images)
            matching_res = self.__match_glyphs_and_encoding_fontforge(os.path.join(img_folders, font_name_images))
            # print(font_file, font_name_images)
            font_name_without_prefix = font_name_images.split('+')[1] if '+' in font_name_images else font_name_images
            dicts[font_name_images] = matching_res if font_name_without_prefix not in dicts else matching_res | \
                                                                                                       dicts[
                                                                                                           font_name_images.split(
                                                                                                               '+')[1]]
        print(dicts)
        # self.match_dict = {**self.match_dict, **dicts}
        # self.match_dict = dicts
        merged_dict = {}
        for key in self.match_dict.keys() | dicts.keys():
            merged_dict[key] = {}
            merged_dict[key].update(self.match_dict.get(key, {}))
            merged_dict[key].update(dicts.get(key, {}))
        self.match_dict = merged_dict
        return self.match_dict

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

    def __match_glyphs_and_encoding_fontforge(self, images):

        images = glob.glob(images + "/*")
        dictionary = {}
        alphas = {}
        maybe_wrong = {}
        for img in images:
            # key = ((img.split('\\')[-1]).split('.')[0]).split('_')[0]
            key = img.split('\\')[-1].split('.')
            key = ''.join(key[:-1])
            # if len(key) == 2:
            #     key = key[0]
            # else:
            #     key = ''.join(key[:-1])
            pred = self.model.recognize_glyph(img)
            char = chr(int(pred))
            try:
                dictionary[chr(int(key))] = chr(int(pred))
                k = chr(int(key))
            except:
                dictionary[key] = chr(int(pred))
                k = key
            if char.isalpha():
                alphas.setdefault(char.lower(), []).append((img, k))
        # for key, value in alphas.items():
        #     if len(value) != 2:
        #         continue
        #     img1 = cv2.imread(value[0][0], cv2.IMREAD_GRAYSCALE)
        #     img2 = cv2.imread(value[1][0], cv2.IMREAD_GRAYSCALE)
        #     white_p1 = np.argwhere(img1 != 0)
        #     white_p2 = np.argwhere(img2 != 0)
        #     if len(white_p1) == 0 or len(white_p2) == 0:
        #         continue
        #     if len(white_p1) > len(white_p2):
        #         dictionary[value[0][1]] = key.upper()
        #         dictionary[value[1][1]] = key.lower()
        #     elif len(white_p1) < len(white_p2):
        #         dictionary[value[0][1]] = key.lower()
        #         dictionary[value[1][1]] = key.upper()

        return dictionary

    def walk(self, o: Any, cached_fonts: dict, fulltext: str):
        if isinstance(o, (LTTextBox, LTTextBoxVertical, LTTextBoxHorizontal)):
            q = 1
        if isinstance(o, LTChar):
            char = o.get_text()
            match_dict_key = self.fontname2basefont[o.fontname]
            if not cached_fonts[o.fontname]:
                try:
                    fulltext += self.match_dict[match_dict_key][char]
                    o._text = self.match_dict[match_dict_key][char]
                    # o._text = '□'
                except:
                    # o._text = char
                    o._text = '□'
                    return
                return
            index = -1
            if 'cid' in char:
                index = int(char[1:-1].split(':')[-1])
            elif 'glyph' in char:
                glyph_unicode = int(char[5:])
                index = ord(self.unicodemaps[glyph_unicode])
            else:
                try:
                    index = ord(char)
                    if ord(char) > len(cached_fonts[o.fontname]) and char == '’':
                        char = "'"
                        index = ord(char)
                    elif ord(char) > len(cached_fonts[o.fontname]):
                        # index = len(cached_fonts[o.fontname])-1
                        o._text = self.match_dict[match_dict_key][char]
                        # o._text = char
                        return
                except:
                    o._text = '□'
                    # o._text += char
                    return
            try:
                glyph_name = cached_fonts[o.fontname][index]
                fulltext += self.match_dict[match_dict_key][glyph_name]
                o._text = self.match_dict[match_dict_key][glyph_name]
            except:
                fulltext += char
                o._text = '□'
        elif isinstance(o, Iterable):
            for i in o:
                self.walk(i, cached_fonts, fulltext)

        if isinstance(o, (LTTextBox, LTTextBoxVertical, LTTextBoxHorizontal)):
            text = o.get_text()
            text = text.replace('\n', ' ')
            text = text.replace('\r', '')
            text = text.replace('\t', ' ')

            # words = re.findall(r'\w+|\S+', text)

            # text = analize.find_closest_word(text)

            self.text += text

