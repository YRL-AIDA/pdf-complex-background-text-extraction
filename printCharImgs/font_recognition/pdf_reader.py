import ast
import os
import re
import shutil
import subprocess
import warnings

import fitz
from PIL import ImageFont
from PIL import Image
from fontTools.agl import toUnicode
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

import config
import main
from image_action import handle_image
from image_action.handle_image import correctly_resize
from font_action.draw_glyph import drawglyph_by_pen
from src.utils import junkstring


class PDFReader:
    def __init__(self, data_save_path):
        self.path = None
        self.fonts_path = config.folders.get('extracted_fonts_folder')
        self.glyphs_path = config.folders.get('extracted_glyphs_folder')
        self.white_spaces = {}

    def read(self, path):
        self.path = path
        self.__extract_fonts()
        # self.__draw_glyphs()
        self.__draw_glyphs_fontforge()
        # self.__draw_glyphs()

    def __draw_glyphs(self):
        if os.path.isdir(self.glyphs_path):
            shutil.rmtree(self.glyphs_path)
        os.makedirs(self.glyphs_path)
        font_files = os.listdir(os.fsencode(self.fonts_path))
        counter = 0
        whitespaces = {}
        for font_file in font_files:
            fontname = os.fsdecode(font_file)
            # font = TTFont(self.fonts_path + "/" + fontname)
            font = TTFont(self.fonts_path + "/" + fontname)
            to_save_folder = fontname.split('.')[0]
            if not os.path.isdir(self.glyphs_path + "/" + to_save_folder):
                os.makedirs(self.glyphs_path + "/" + to_save_folder)

            charlist = font.getGlyphSet()
            glyphset = font.getGlyphSet()

            size = 0
            minsize = 10000

            cmap = {}
            if 'cmap' in font:
                cmap = {j: i for i, j in zip(font['cmap'].tables[0].cmap, font['cmap'].tables[0].cmap.values())}
                charlist = [j for j in font['cmap'].tables[0].cmap.values()]
            # print("cmap",cmap)
            # print("list:",charlist)
            # for g in glyphset:
            #     bp = BoundsPen(glyphset)
            #     glyph = glyphset[g]
            #     glyph.draw(bp)
            #     if bp.bounds is None:
            #         continue
            #     size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            #     minsize = min(minsize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            font_whitespaces = []
            # print(fontname)
            for g in charlist:
                img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, minsize=minsize)
                # if img is None:
                #     # font_whitespaces.append(pngname)
                #     continue
                if g[0] == '.':
                    continue
                if cmap:
                    g = chr(cmap[g])
                if 'glyph' in g:
                    continue
                if 'uni' in g:
                    g = toUnicode(g)
                pngname = str(ord(g))
                if img is None:
                    font_whitespaces.append(chr(int(pngname)))
                    continue
                img.save(self.glyphs_path + "/" + to_save_folder + "/" + pngname + ".png")
                counter += 1
            whitespaces[fontname.split('.')[0]] = font_whitespaces


        # print("reader whitespaces", whitespaces)
        self.white_spaces = whitespaces

    def __draw_glyphs_fontforge(self):
        if os.path.isdir(self.glyphs_path):
            shutil.rmtree(self.glyphs_path)
        os.makedirs(self.glyphs_path)
        font_files = os.listdir(os.fsencode(self.fonts_path))
        DEVNULL = open(os.devnull, 'wb')
        white_spaces = {}
        for font_file in font_files:
            font_white_spaces = {}
            fontname = os.fsdecode(font_file)
            print("fontname", fontname)
            fontname = fontname.split('.')[0]
            fontname = re.split(junkstring, fontname)[0]
            print("split", re.split(junkstring, fontname))
            save_path = f"{self.glyphs_path}/{fontname}"
            if not os.path.isdir(save_path):
                os.makedirs(save_path)
            font_path = fr'"{self.fonts_path}/{os.fsdecode(font_file)}"'
            save_path = fr'"{save_path}"'
            warnings.warn('glyph#### how to parse')
            result = subprocess.check_output(f"ffpython ../font_action/fontforge_wrapper.py False {save_path} {font_path}")
            result = result.decode('utf-8')
            result = set(ast.literal_eval(result))
            for img in result:
                if handle_image.is_empty(img) and img.split('.')[-1] == 'png':
                    uni_whitespace = img.split('/')[-1].split('.')[0]
                    name = ''
                    try:
                        name = chr(int(uni_whitespace))
                    except:
                        name = uni_whitespace
                    if name == '■': #278.json
                        q = 1
                    font_white_spaces[name] = ' '
                    os.remove(img)
                    continue
                correctly_resize(img)
            white_spaces[fontname] = font_white_spaces
        self.white_spaces = white_spaces
        print("whitespaces", self.white_spaces)

    def __extract_fonts(self):
        if os.path.isdir(self.fonts_path):
            shutil.rmtree(self.fonts_path)
        os.makedirs(self.fonts_path)
        doc = fitz.open(self.path)
        xref_visited = []

        # что блять
        dir = self.fonts_path + "/"
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)
        ###
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
                # if font['ext'] != "n/a" and font['ext'] != 'cff':
                # if font['ext'] != "n/a":
                # if font['ext'] in ["otf", "ttf"]:
                #     ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                #     # ofile = open(dir + font['name'] + "." + 'otf', "wb")
                #     ofile.write(font['content'])
                #     ofile.close()
                if font['ext'] != 'n/a':
                    # ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                    ofile = open(dir + font['name'] + junkstring + str(junk) + "." + font['ext'], "wb")
                    # ofile = open(dir + font['name'] + "." + 'otf', "wb")
                    ofile.write(font['content'])
                    ofile.close()
        doc.close()

    def get_glyphs_path(self):
        return self.glyphs_path

    def get_fonts_path(self):
        return self.fonts_path
