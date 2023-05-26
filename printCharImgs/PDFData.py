import configparser
import glob
import os
import shutil
from collections import OrderedDict
from copy import copy

import fitz
from PIL import ImageFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer,  LTChar

from CNN_modelclass import recognize_glyph
from DrawGlyph import drawglyph_by_pen, drawglyph_pillow
from Analize import correct_text

config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')
# config.read('config.ini', encoding='utf-8')

invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
inv_map = {v: k for k, v in invalid_symbols.items()}
invalid_symbolsnoregdiff = eval(config.get("DEFAULT", "invalidSymbolsnoregdiff"))
inv_mapnoregdiff = {v: k for k, v in invalid_symbolsnoregdiff.items()}
eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def __draw_glyphs(save_path="pdfdata/glyphimages", fonts_path="pdfdata/extracted_font"):
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
    fonts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fonts_path)
    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    font_files = os.listdir(os.fsencode(fonts_path))
    counter = 0
    for font_file in font_files:
        fontname = os.fsdecode(font_file)
        font = TTFont(fonts_path + "/" + fontname)
        tosavefolder = fontname.split('.')[0]
        # tosavefolder = tosavefolder.split('+')[1]
        f1 = ImageFont.truetype(fonts_path + "/" + fontname, 18)
        # font = ttLib.SFNTReader(fonts_path + "/" + fontname)
        # font = fontTools.cffLib.CFFFontSet.convertCFFToCFF2(fonts_path + "/" + fontname)
        if not os.path.isdir(save_path + "/" + tosavefolder):
            os.makedirs(save_path + "/" + tosavefolder)
        glyphset = font.getGlyphSet()
        size = 0
        minsize = 10000
        gg = ""
        # print(tosavefolder)
        l = []
        if tosavefolder == 'BHSASO+TimesNewRomanPSMT':
            continue
        for g in glyphset:
            bp = BoundsPen(glyphset)
            glyph = glyphset[g]
            glyph.draw(bp)
            if bp.bounds is None:
                continue
            if size > abs(bp.bounds[1]) + abs(bp.bounds[3]):
                gg = g
            size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            minsize = min(minsize, abs(bp.bounds[1]) + abs(bp.bounds[3]))

        # print(minsize / size, minsize, size)
        for g in glyphset:

            img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, minsize=minsize)
            # img = drawglyph_pillow(pfont, pfont.glyph_name_to_unicode(g), (28, 28))
            if img is None:
                continue
            if g[0] == '.':
                continue
            # print(g)
            l.append(g)
            pngname = g + "_lower" if g.islower() else g + "_upper" if g.isupper() else g
            # img.show()
            img.save(save_path + "/" + tosavefolder + "/" + pngname + ".png")
            counter += 1
        # l.sort()
        # print(l)


def __extract_pfdfonts(pdf_path, save_path="pdfdata/extracted_font"):
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
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
        for fontinfo in page:
            xref = fontinfo[0]
            if xref in xref_visited:
                continue
            xref_visited.append(xref)
            font = doc.extract_font(xref, named=True)
            # print(font['name'], font['ext'])
            # name = font['name'].split("+", 1)[1] if "+" in font['name'] else font['name']
            if font['ext'] != "n/a":
                ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                ofile.write(font['content'])
                ofile.close()
    doc.close()


def func(pdf_path):
    doc = fitz.open(pdf_path)
    xref_visited = []
    for page_num in range(doc.page_count):
        page = doc.get_page_fonts(page_num)
        page = doc.get_page_fonts(page_num)
        for fontinfo in page:
            xref = fontinfo[0]
            if xref in xref_visited:
                continue
            xref_visited.append(xref)
            font = doc.extract_font(xref, named=True)
            if font['name'] == 'VGPRFL+TimesNewRoman,Bold':
                print("123")
                doc[page_num].insert_font(fontname="VGPRFL+TimesNewRoman,Bold",
                                          fontfile="pdfdata/extracted_font/VGPRFL+TimesNewRoman,Bold.ttf")
            if font['name'] == 'ATSFPL+TimesNewRoman,BoldItalic':
                print("123")
                doc[page_num].insert_font(fontname="ATSFPL+TimesNewRoman,BoldItalic",
                                          fontfile="pdfdata/extracted_font/ATSFPL+TimesNewRoman,BoldItalic.ttf")
            if font['name'] == 'FCDHEK+TimesNewRoman,Italic':
                print("123")
                doc[page_num].insert_font(fontname="FCDHEK+TimesNewRoman,Italic",
                                          fontfile="pdfdata/extracted_font/FCDHEK+TimesNewRoman,Italic.ttf")
            if font['name'] == 'MVVIUJ+TimesNewRoman':
                print("123")
                doc[page_num].insert_font(fontname="MVVIUJ+TimesNewRoman",
                                          fontfile="pdfdata/extracted_font/MVVIUJ+TimesNewRoman.ttf")
            if font['name'] == 'OPEHOG+TimesET,Italic':
                print("123")
                doc[page_num].insert_font(fontname="OPEHOG+TimesET,Italic",
                                          fontfile="pdfdata/extracted_font/OPEHOG+TimesET,Italic.ttf")
    doc.save("123.pdf")
    doc.close()


def __match_glyphs_and_encoding(ttffont, fitzfont, images):
    images = glob.glob(images + "/*")
    dict = {}
    # cmap14 = CmapSubtable.newSubtable(14)
    inv_cmap = {i: fitzfont.glyph_name_to_unicode(i) for i in ttffont.getGlyphNames()}

    # print(inv_cmap)
    # print(cmap)
    for img in images:
        key = ((img.split('\\')[-1]).split('.')[0]).split('_')[0]
        if key not in inv_cmap:
            continue
        pred = recognize_glyph(img)
        key = chr(inv_cmap[key])
        # print(key)
        # if pred in inv_map:
        #     name = inv_map[pred]
        if pred in inv_mapnoregdiff:
            name = inv_mapnoregdiff[pred]
        else:
            name = pred
        dict[key] = name
    # cmap14.platformID = 3
    # cmap14.platEncID = 10
    # # cmap14.language = 0
    # cmap14.cmap = dict
    # cmap = newTable("cmap")
    # cmap.tableVersion = 0
    # cmap.tables = [cmap14]
    # font['cmap'] = cmap
    # print(font.getBestCmap())
    # return font.getBestCmap()
    return dict


def __match_glyphs_and_encoding_forall():
    imgfolders = "pdfdata/glyphimages/"
    imgfolders = os.path.join(os.path.dirname(os.path.abspath(__file__)), imgfolders)
    extracted_fonts_folder = "pdfdata/extracted_font/*"
    extracted_fonts_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), extracted_fonts_folder)
    fonts = glob.glob(extracted_fonts_folder)
    dicts = {}
    for fontfile in fonts:
        fontname = fontfile.split('\\')[-1]
        ttffont = TTFont(fontfile)
        fitzfont = fitz.Font(fontfile=fontfile)
        fontnameimgs = fontname.split('.')[0]
        # dicts[fontnameimgs] = __match_glyphs_and_encoding(ttffont, fitzfont, imgfolders + fontnameimgs)
        dicts[fontnameimgs.split('+')[1]] = __match_glyphs_and_encoding(ttffont, fitzfont, imgfolders + fontnameimgs)
    # print(dicts)
    return dicts


def __gettextfrompdf(pdf_path, dictionary):
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        sentence = ""
        for blocks in page.get_text("dict")['blocks']:
            try:
                for lines in blocks['lines']:
                    for spans in lines['spans']:
                        for index, char in enumerate(spans['text']):
                            try:
                                sentence += dictionary[spans['font']][char]
                            except KeyError:
                                sentence += char
                    sentence += "\n"
            except KeyError:
                pass
        text.append(sentence)
        break
    return text


def __save_pdf_as_txt(pdf_path):
    name = pdf_path.split('/')[-1].split('.')[0]
    shutil.copyfile(pdf_path, "pdfdata/" + name + ".txt")
    path = "pdfdata/" + name + ".txt"
    return path

def get_encoding(txt_path):
    ofile = open(txt_path, "rb")
    fc = str.encode('FirstChar')
    lc = str.encode('LastChar')
    fontname1 = str.encode('/BaseFont /')
    fontname2 = str.encode('/FontFile')
    fontname3 = str.encode('/FontName')
    fcl = []
    lcl = []
    fontnamel = []

    for i in ofile:
        if fc in i:
            nametoadd = i.decode().split(' ')[-1].split('\n')[0]
            fcl.append(nametoadd)
        if lc in i:
            nametoadd = i.decode().split(' ')[-1].split('\n')[0]
            lcl.append(nametoadd)
        if fontname1 in i or fontname2 in i or fontname3 in i:
            fontnametoadd = i.decode()
            # print(fontnametoadd)
            if '+' not in fontnametoadd:
                continue
            fontnametoadd = fontnametoadd.split(' ')[-1].split('/')[-1].split('\n')[0]
            fontnamel.append(fontnametoadd)
    from collections import OrderedDict
    # dict = {name: (x, charsinSymbols) for name, x, y in zip(fontnamel, fcl, lcl)}
    dict = {name: x for name, x in zip(fontnamel, fcl)}
    return dict


def getCharsOfFonts(pdf_path):
    charsinSymbols = {}
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text()
                for text_line in element:
                    try:
                        for char in text_line:
                            try:
                                if isinstance(char, LTChar):
                                    text = text.replace(' ', '')
                                    text = text.replace('\n', '')
                                    if char.fontname not in charsinSymbols.keys():
                                        charsinSymbols[char.fontname] = list(text)
                                    else:
                                        charsinSymbols[char.fontname] = charsinSymbols[char.fontname] + list(text)
                                    break
                            except:
                                pass
                    except:
                        pass
    for i in charsinSymbols.keys():
        charsinSymbols[i] = list(OrderedDict.fromkeys(charsinSymbols[i]))
    return charsinSymbols


def gettext(pdf_path):
    txt_path = __save_pdf_as_txt(pdf_path)
    firstchars = get_encoding(txt_path)
    charsOffonts = getCharsOfFonts(pdf_path)
    __extract_pfdfonts(pdf_path)
    __draw_glyphs()
    text = __gettextfrompdf(pdf_path, __match_glyphs_and_encoding_forall())
    # return correct_text(text)
