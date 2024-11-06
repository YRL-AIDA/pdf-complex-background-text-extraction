import ast
import glob
import os
import re
import shutil
import subprocess
import warnings
from pathlib import Path
from typing import Any, Iterable

import fitz

import config
from model.model import Model
from pdf_worker import pdf_text_correcter
from utils import functions
from utils.functions import junk_string, correctly_resize

from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTChar, LTPage, LTTextBox, LTTextBoxHorizontal, LTTextBoxVertical
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral


class PDFReader:
    def __init__(self, model: Model):
        self.extract_path = config.folders.get('extracted_data_folder')
        self.model = model
        self.text = None
        self.match_dict = {}
        self.__cached_fonts = None
        self.__fontname2basefont = {}
        self.__unicodemaps = {}
        self.__need2correct = False

        self.__fonts_path = config.folders.get('extracted_fonts_folder')
        self.__glyphs_path = config.folders.get('extracted_glyphs_folder')

        assert len(self.model.labels) > 0

        rus = False
        eng = False
        for i in self.model.labels:
            if ord('a') <= i <= ord('z'):
                eng = True

            elif ord('а') <= i <= ord('я'):
                rus = True

            if rus and eng:
                self.__need2correct = True
                break


    @classmethod
    def load_default_model(cls, default_model: config.DefaultModel = config.DefaultModel.Russian_and_English):
        new_model = Model.load_default_model(default_model=default_model)
        new_model.default_model = default_model
        reader = cls(model=new_model)
        return reader

    @classmethod
    def load_model(cls, model_and_labels_path: Path):
        """
        h5/keras and json with model's labels should be in folder
        """
        assert len([name for name in model_and_labels_path.iterdir() if model_and_labels_path.joinpath(name).is_file()]) == 2,\
            "should be two files in folder: h5, json"

        new_model = Model.load_by_model_and_labels_folder(model_and_labels_path)
        return cls(new_model)

    def restore_text(self, pdf_path: Path, start_page: int = 0, end_page: int = 0) -> str:
        assert end_page > start_page or start_page == end_page == 0, "wrong pages range"
        self.text = ''
        self.match_dict = {}

        self.__read_pdf(pdf_path)

        warnings.warn('self.match_dict = self.reader.white_spaces ????')
        warnings.warn('right now ignoring #.superior')

        self.__match_glyphs_and_encoding_for_all()
        fonts_match_dict = self.match_dict
        self.text = self.__restore_text(pdf_path, start=start_page, end=end_page)
        self.text = re.sub(r'\s+', ' ', self.text)
        if self.__need2correct:
            self.text = pdf_text_correcter.correct_collapsed_text(self.text)
        return self.text

    def __read_pdf(self, pdf_path: Path):
        self.__extract_fonts(pdf_path)
        self.__extract_glyphs()

    def __extract_fonts(self, pdf_path: Path):
        if os.path.isdir(self.__fonts_path):
            shutil.rmtree(self.__fonts_path)
        os.makedirs(self.__fonts_path)
        doc = fitz.open(pdf_path)
        xref_visited = []

        junk = 0
        for page_num in range(doc.page_count):
            page = doc.get_page_fonts(page_num)
            for fontinfo in page:
                junk += 1
                xref = fontinfo[0]
                if xref in xref_visited:
                    continue
                xref_visited.append(xref)
                font = doc.extract_font(xref, named=True)
                print(page_num, font['name'], font['ext'])
                if font['ext'] != 'n/a':
                    # font_path = self.__fonts_path.joinpath(font['name'] + junk_string + str(junk) + '.' + font['ext'])
                    font_path = self.__fonts_path.joinpath(f"{font['name']}{junk_string}{str(junk)}.{font['ext']}")
                    ofile = open(font_path, 'wb')
                    ofile.write(font['content'])
                    ofile.close()
        doc.close()

    def __extract_glyphs(self):
        if os.path.isdir(self.__glyphs_path):
            shutil.rmtree(self.__glyphs_path)
        os.makedirs(self.__glyphs_path)
        font_files = os.listdir(os.fsencode(self.__fonts_path))
        DEVNULL = open(os.devnull, 'wb')
        white_spaces = {}
        for font_file in font_files:
            font_white_spaces = {}
            font_name = os.fsdecode(font_file)
            print("fontname", font_name)
            font_name = font_name.split('.')[0]
            font_name = re.split(junk_string, font_name)[0]
            print("split", re.split(junk_string, font_name))
            save_path = self.__glyphs_path.joinpath(font_name)
            if not os.path.isdir(save_path):
                os.makedirs(save_path)
            font_path = self.__fonts_path.joinpath(os.fsdecode(font_file))
            warnings.warn('glyph#### how to parse')
            result = subprocess.check_output(f"ffpython ../font_action/fontforge_wrapper.py False {save_path} {font_path}")
            result = result.decode('utf-8')
            result = set(ast.literal_eval(result))
            for img in result:
                correctly_resize(img)
            white_spaces[font_name] = font_white_spaces
        self.white_spaces = white_spaces
        print("whitespaces", self.white_spaces)

    def __match_glyphs_and_encoding_for_all(self):
        extracted_fonts_folder = config.folders.get("extracted_fonts_folder")
        fonts = glob.glob(extracted_fonts_folder + "/*")
        dicts = {}
        for font_file in fonts:
            fontname = font_file.split('\\')[-1]
            font_name_images = fontname.split('.')[0]
            font_name_images = font_name_images.split(junk_string)[0]
            print("fontnameimgs", font_name_images)
            matching_res = self.__match_glyphs_and_encoding(self.__glyphs_path.joinpath(font_name_images))
            font_name_without_prefix = font_name_images.split('+')[1] if '+' in font_name_images else font_name_images
            dicts[font_name_images] = matching_res if font_name_without_prefix not in dicts \
                else matching_res | dicts[font_name_images.split('+')[1]]

    def __match_glyphs_and_encoding(self, images_path: Path):

        # images_path = glob.glob(images_path + "/*")
        images = images_path.glob("*")
        dictionary = {}
        alphas = {}
        for img in images:
            # key = img.split('\\')[-1].split('.')
            key = img.parts[-1].split('.')
            key = ''.join(key[:-1])
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

        return dictionary

    def __restore_text(self, pdf_path, start=0, end=0):
        fulltext = ''
        self.__cached_fonts = None
        self.__fontname2basefont = {}
        self.__unicodemaps = {}
        with open(pdf_path, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            pages_count = resolve1(document.catalog['Pages'])['Count']
            end = pages_count if end == 0 else end

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
                    self.__fontname2basefont[f.fontname] = f.basefont if hasattr(f, 'basefont') else f.fontname

                    if hasattr(f, 'unicode_map') and hasattr(f.unicode_map, 'cid2unichr'):
                        basefont_else_fontname = self.__fontname2basefont[f.fontname]
                        self.__unicodemaps[basefont_else_fontname] = f.unicode_map.cid2unichr
                    if not (isinstance(encoding, dict) and ('/Differences' in encoding or 'Differences' in encoding)):
                        cached_fonts[f.fontname] = []
                        continue
                    char_set_arr = [q.name if isinstance(q, PSLiteral) else '' for q in encoding['Differences']]
                    cached_fonts[f.fontname] = char_set_arr
                self.__cached_fonts = rsrcmgr._cached_fonts
                self.walk_pdf(layout, cached_fonts, fulltext)
        self.text = functions.remove_hyphenations(self.text)
        return self.text

    def walk_pdf(self, o: Any, cached_fonts: dict, fulltext: str):
        if isinstance(o, LTChar):
            char = o.get_text()
            match_dict_key = self.__fontname2basefont[o.fontname]
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
                index = ord(self.__unicodemaps[glyph_unicode])
            else:
                try:
                    index = ord(char)
                    if ord(char) > len(cached_fonts[o.fontname]) and char == '’':
                        char = "'"
                        index = ord(char)
                    elif ord(char) > len(cached_fonts[o.fontname]):
                        o._text = self.match_dict[match_dict_key][char]
                        return
                except:
                    o._text = '□'
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
                self.walk_pdf(i, cached_fonts, fulltext)

        if isinstance(o, (LTTextBox, LTTextBoxVertical, LTTextBoxHorizontal)):
            text = o.get_text()
            text = text.replace('\n', ' ')
            text = text.replace('\r', '')
            text = text.replace('\t', ' ')
            self.text += text

    def save_text(self, save_path: Path):
        with open(save_path, "w") as f:
            f.write(self.text)

