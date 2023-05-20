from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import os
import shutil
import fitz
from fontTools.ttLib import TTFont

from DrawGlyph import drawglyph_by_pen
from CNN_modelclass import recognize_glyph
import glob
import configparser
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.ttLib.ttFont import newTable
from PIL import Image, ImageFont, ImageDraw, ImageOps


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
inv_map = {v: k for k, v in invalid_symbols.items()}

def __draw_glyphs(save_path="pdfdata/glyphimages", fonts_path="pdfdata/extracted_font"):
    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    font_files = os.listdir(os.fsencode(fonts_path))
    counter = 0
    for font_file in font_files:
        fontname = os.fsdecode(font_file)
        font = TTFont(fonts_path + "/" + fontname)
        f1 = ImageFont.truetype(fonts_path + "/" + fontname, 18)
        # font = ttLib.SFNTReader(fonts_path + "/" + fontname)
        # font = fontTools.cffLib.CFFFontSet.convertCFFToCFF2(fonts_path + "/" + fontname)
        os.makedirs(save_path + "/" + fontname)
        glyphset = font.getGlyphSet()
        size = 0
        # size = 0, 0
        for g in glyphset:
            bp = BoundsPen(glyphset)
            glyph = glyphset[g]
            glyph.draw(bp)
            if bp.bounds is None:
                continue

            # ranshe size bil tolko dly height menya tut i v drawglyph_by_pen
            if bp.bounds[1] < 0:
                # size = max(size[0], abs(bp.bounds[0]) + abs(bp.bounds[2])), \
                #        max(size[1], abs(bp.bounds[1]) + abs(bp.bounds[3]))
                size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
        for g in glyphset:

            ## method mb nado raskomentit budet tak chto poka tak

            # pen = FreeTypePen(glyphset)
            # bp = BoundsPen(glyphset)
            # glyph = glyphset[g]
            # glyph.draw(pen)
            # glyph.draw(bp)
            # if bp.bounds is None:
            #     continue
            # # img = pen.image(width=glyph.width, height=abs(bp.bounds[1] + bp.bounds[3]), contain=True)
            # if bp.bounds[1] > 0:
            #     img = pen.image(width=glyph.width, height=(bp.bounds[1] + bp.bounds[3])/2, contain=True)
            # else:
            #     # img = pen.image(width=glyph.width, height=1300, contain=True)
            #     img = pen.image(width=glyph.width, height=size, contain=True)
            #     # img = pen.image(width=glyph.width, height= (abs(bp.bounds[1]) + abs(bp.bounds[3]))+500, contain=True)
            # # img = pen.image(width=abs(bp.bounds[0] + bp.bounds[2]), height=abs(bp.bounds[1] + bp.bounds[3])*2)
            # # img = pen.image(width=glyph.width, height=abs(bp.bounds[1] + bp.bounds[3]), contain=True)
            # background = Image.new('LA', img.size, (255, 255))
            # alpha_composite = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
            # alpha_composite = alpha_composite.convert("L")
            # # alpha_composite = alpha_composite.resize((20, 20))
            # alpha_composite.thumbnail((28, 28))
            # alpha_composite = ImageOps.invert(alpha_composite)
            # # alpha_composite = alpha_composite.resize((20, 20))
            # img = alpha_composite
            # new_im = Image.new("L", (28, 28))
            # box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
            # new_im.paste(img, box)
            # img = new_im
            # img.save(save_path + "/" + fontname + "/" + str(counter) + ".png")

            ## method
            img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, counter=counter)

            if img is None:
                continue
            img.save(save_path + "/" + fontname + "/" + g + ".png")
            counter += 1


def __extract_pfdfonts(pdf_path, save_path="pdfdata/extracted_font"):
    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    doc = fitz.open(pdf_path)
    xref_visited = []
    dir = save_path + "/"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    for page_num in range(doc.page_count):
        page = doc.get_page_fonts(page_num)
        # print(page)
        for fontinfo in page:
            xref = fontinfo[0]
            if xref in xref_visited:
                continue
            xref_visited.append(xref)
            # name, ext, _, content = doc.extract_font(xref, named=True)
            font = doc.extract_font(xref, named=True)
            # print(font)
            # name = name.split("+", 1)[1] if "+" in name else name
            if font['ext'] != "n/a":
                ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                # print(dir + font['name'] + "." + font['ext'])
                ofile.write(font['content'])
                ofile.close()
    doc.close()


def __match_glyphs_and_encoding(font, images):
    images = glob.glob(images + "/*")
    # ne vidit .notdef (.)
    dict = {}
    cmap14 = CmapSubtable.newSubtable(14)
    for img in images:
        pred = recognize_glyph(img)
        if pred in inv_map:
            key = ord(inv_map[pred])
            # name = inv_map[pred]
        else:
            key = ord(pred)
            # name = pred
        name = img.split('\\')[-1]
        name = name.split('.')[0]
        dict[key] = name
    cmap14.platformID = 3
    cmap14.platEncID = 10
    # cmap14.language = 0
    cmap14.cmap = dict
    cmap = newTable("cmap")
    cmap.tableVersion = 0
    cmap.tables = [cmap14]
    font['cmap'] = cmap
    print(font.getBestCmap())


def __match_glyphs_and_encoding_forall():
    imgfolders = "pdfdata/glyphimages/"
    extracted_fonts_folder = "pdfdata/extracted_font/*"
    fonts = glob.glob(extracted_fonts_folder)
    for fontfile in fonts:
        fontname = fontfile.split('\\')[-1]
        font = TTFont(fontfile)
        __match_glyphs_and_encoding(font, imgfolders + fontname)

def restore_encoding(pdf_path):
    # __extract_pfdfonts(pdf_path)
    # __draw_glyphs()
    # __match_glyphs_and_encoding()
    __match_glyphs_and_encoding_forall()
