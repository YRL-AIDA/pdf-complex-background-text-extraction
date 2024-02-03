import os
import shutil

import fitz
from PIL import ImageFont
from fontTools.agl import toUnicode
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

import config
import main
from font_action.draw_glyph import drawglyph_by_pen

class PDFReader:
    def __init__(self, data_save_path):
        self.path = None
        self.fonts_path = config.folders.get('extracted_fonts_folder')
        self.glyphs_path = config.folders.get('extracted_glyphs_folder')
        self.white_spaces = {}

    def read(self, path):
        self.path = path
        self.__extract_fonts()
        self.__draw_glyphs()

    def __draw_glyphs(self):
        if os.path.isdir(self.glyphs_path):
            shutil.rmtree(self.glyphs_path)
        os.makedirs(self.glyphs_path)
        font_files = os.listdir(os.fsencode(self.fonts_path))
        counter = 0
        whitespaces = {}
        for font_file in font_files:
            fontname = os.fsdecode(font_file)
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
            # print(charlist)
            for g in charlist:
                img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, minsize=minsize)
                # if img is None:
                #     # font_whitespaces.append(pngname)
                #     continue
                if g[0] == '.':
                    continue

                if cmap:
                    g = chr(cmap[g])
                if 'uni' in g:
                    g = toUnicode(g)
                pngname = str(ord(g))
                if img is None:
                    font_whitespaces.append(chr(int(pngname)))
                    continue
                # elif g in invalid_symbols:
                #     g = invalid_symbols[g]
                # pngname = g + "_lower" if g.islower() else g + "_upper" if g.isupper() else g
                img.save(self.glyphs_path + "/" + to_save_folder + "/" + pngname + ".png")
                counter += 1
            whitespaces[fontname.split('.')[0]] = font_whitespaces

        print(whitespaces)
        self.white_spaces = whitespaces

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

        for page_num in range(doc.page_count):
            page = doc.get_page_fonts(page_num)
            for fontinfo in page:
                xref = fontinfo[0]
                if xref in xref_visited:
                    continue
                xref_visited.append(xref)
                font = doc.extract_font(xref, named=True)
                if font['ext'] != "n/a" and font['ext'] != 'cff':
                    ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                    ofile.write(font['content'])
                    ofile.close()
        doc.close()

    def get_glyphs_path(self):
        return self.glyphs_path

    def get_fonts_path(self):
        return self.fonts_path

