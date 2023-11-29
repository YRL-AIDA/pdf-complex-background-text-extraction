import configparser
import glob
import os
import shutil
from collections import OrderedDict
import fitz
from PIL import ImageFont
# from PyPDF2 import PdfReader
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer,  LTChar
from fontTools.agl import toUnicode

# from CNN_modelclass import CNN
from CNN_modelclass import CNN
from font_recognition.draw_glyph import drawglyph_by_pen
from Analize import correct_text

config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')
# config.read('config.ini', encoding='utf-8')

invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
inv_map = {v: k for k, v in invalid_symbols.items()}
invalid_symbolsnoregdiff = eval(config.get("DEFAULT", "invalidSymbolsnoregdiff"))
inv_mapnoregdiff = {v: k for k, v in invalid_symbolsnoregdiff.items()}
fitz.TOOLS.set_subset_fontnames(True)
global parts
parts = []
global cnn

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
        # print(tosavefolder)
        f1 = ImageFont.truetype(fonts_path + "/" + fontname, 18)
        # font = ttLib.SFNTReader(fonts_path + "/" + fontname)
        # font = fontTools.cffLib.CFFFontSet.convertCFFToCFF2(fonts_path + "/" + fontname)
        if not os.path.isdir(save_path + "/" + tosavefolder):
            os.makedirs(save_path + "/" + tosavefolder)


        charlist = font.getGlyphSet()
        glyphset = font.getGlyphSet()

        size = 0
        minsize = 10000

        cmap = {}
        if 'cmap' in font:
            cmap = {j: i for i, j in zip(font['cmap'].tables[0].cmap, font['cmap'].tables[0].cmap.values())}
            charlist = [j for j in font['cmap'].tables[0].cmap.values()]
        for g in glyphset:
            bp = BoundsPen(glyphset)
            glyph = glyphset[g]
            glyph.draw(bp)
            if bp.bounds is None:
                continue
            size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            minsize = min(minsize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
        for g in charlist:
            img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, minsize=minsize)
            # img = drawglyph_pillow(pfont, pfont.glyph_name_to_unicode(g), (28, 28))
            if img is None:
                continue
            if g[0] == '.':
                continue

            if cmap:
                g = chr(cmap[g])
            if 'uni' in g:
                g = toUnicode(g)
            elif g in invalid_symbols:
                g = invalid_symbols[g]
            pngname = g + "_lower" if g.islower() else g + "_upper" if g.isupper() else g
            img.save(save_path + "/" + tosavefolder + "/" + pngname + ".png")
            counter += 1


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
            if font['ext'] != "n/a" and font['ext'] != 'cff':
                ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                ofile.write(font['content'])
                ofile.close()
    doc.close()


def __match_glyphs_and_encoding(ttffont, fitzfont, images, mode):
    images = glob.glob(images + "/*")
    dict = {}
    if 'cmap' in ttffont:
        # inv_cmap = {toUnicode(j) if 'uni' in j else j: i for i, j in zip(ttffont['cmap'].tables[0].cmap, ttffont['cmap'].tables[0].cmap.values())}
        # for i in ttffont['cmap'].tables[0].cmap:
        #     print(type(i))
        # codes = [x for x in ttffont['cmap'].tables[0].cmap]
        # print(chr(codes[0]))
        inv_cmap = {i: toUnicode(j) if 'uni' in j else j for i, j in zip(ttffont['cmap'].tables[0].cmap, ttffont['cmap'].tables[0].cmap.values())}
    else:
        inv_cmap = {i: fitzfont.glyph_name_to_unicode(i) for i in ttffont.getGlyphNames()}

    # print(inv_cmap)
    # print(cmap)
    for img in images:
        key = ((img.split('\\')[-1]).split('.')[0]).split('_')[0]
        pred = cnn.recognize_glyph(img)
        if key in inv_cmap:
            key = chr(inv_cmap[key])

        if pred in inv_mapnoregdiff:
            name = inv_mapnoregdiff[pred]
        else:
            name = pred
        # print(key)
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
    # print(dict)
    return dict


def __match_glyphs_and_encoding_forall(mode):
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
        matchingres = __match_glyphs_and_encoding(ttffont, fitzfont, imgfolders + fontnameimgs, mode)
        # dicts[fontnameimgs.split('+')[1]] = matchingres if fontnameimgs.split('+')[1] not in dicts else matchingres | dicts[fontnameimgs.split('+')[1]]
        dicts[fontnameimgs] = matchingres if fontnameimgs.split('+')[1] not in dicts else matchingres | dicts[fontnameimgs.split('+')[1]]
        # print(matchingres | dicts[fontnameimgs.split('+')[1]])
    print(dicts)
    return dicts


def __gettextfrompdf(pdf_path, dictionary, start=0, end=0):
    doc = fitz.open(pdf_path)
    text = []
    if end == 0:
        end = doc.page_count
    pages = [doc[i] for i in range(start, end)]
    for page in pages:
        sentence = ""
        for blocks in page.get_text("dict")['blocks']:
            try:
                for lines in blocks['lines']:
                    linetext = ""
                    for spans in lines['spans']:
                        word = ""
                        for index, char in enumerate(spans['text']):
                            try:
                                if char in invalid_symbolsnoregdiff:
                                    word += dictionary[spans['font']][invalid_symbolsnoregdiff[char]]
                                    # sentence += dictionary[spans['font']][invalid_symbolsnoregdiff[char]]
                                elif char in dictionary[spans['font']]:
                                    word += dictionary[spans['font']][char]
                                    # sentence += dictionary[spans['font']][char]
                                else:
                                    # sentence += dictionary[spans['font']][char]
                                    word += char
                                    # sentence += char
                            except KeyError:
                                word += char
                                # sentence += char
                        linetext += word
                        # print(word)
                        # word = word.lstrip(' ')
                        # sentence += word
                    linetext = linetext.lstrip(' ')
                    sentence += linetext
                    sentence += "\n"
            except KeyError:
                pass
        text.append(sentence)
    return text

    # reader = PdfReader(pdf_path)
    # pages = []
    # text = []
    # pagestoread = [reader.pages[i] for i in range(start, end)]
    # for page in pagestoread:
    #     global parts
    #     parts = []
    #     page.extract_text(visitor_text=visitor_body)
    #     pages.append(parts)
    # # print(pages)
    # for page in pages:
    #     pagetext = ""
    #     for i in page:
    #         curtext = ""
    #         # print(i)
    #         line = ""
    #         for char in i[1]:
    #             try:
    #                 # if char == ' ' or char == '\n':
    #                 #     pagetext += char
    #                 if char in invalid_symbolsnoregdiff:
    #                     pagetext += dictionary[i[0]][invalid_symbolsnoregdiff[char]]
    #                     line +=  dictionary[i[0]][invalid_symbolsnoregdiff[char]]
    #                     # curtext += dictionary[i[0]][invalid_symbolsnoregdiff[char]]
    #                 elif char in dictionary[i[0]]:
    #                     pagetext += dictionary[i[0]][char]
    #                     line += dictionary[i[0]][char]
    #                     # curtext += dictionary[i[0]][char]
    #                 else:
    #                     # pagetext += dictionary[i[0]][char]
    #                     pagetext += char
    #                     line += char
    #                     # curtext += char
    #             except KeyError:
    #                 pagetext += char
    #                 line += char
    #         # if line != '\n' and not line.isspace():
    #         #     print(line)
    #         print('line', line)
    #         # print(" " + curtext + " ")
    #         pagetext += "\n"
    #     # print(pagetext)
    #     text.append(pagetext)
    # return text
    # print(text_body)



# def __save_pdf_as_txt(pdf_path):
#     name = pdf_path.split('/')[-1].split('.')[0]
#     # shutil.copyfile(pdf_path, "pdfdata/" + name + ".txt")
#     path = "pdfdata/" + name + ".txt"
#     return path

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
            if '+' not in fontnametoadd:
                continue
            fontnametoadd = fontnametoadd.split(' ')[-1].split('/')[-1].split('\n')[0]
            fontnamel.append(fontnametoadd)
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


# def __match_glyphnames2chars(pdf_path):
#     fd = open(pdf_path, "rb")
#     doc = PDFDocument(fd)
#     fonts = {}
#     for page in doc.pages():
#         fonts = fonts | page.Resources.Font
#     fontfiles = glob.glob("pdfdata/extracted_font")
#     ttfonts = {}
#     for fontfile in fontfiles:
#         ttfonts[fontfile.split('\\')[-1].split('.')[0]] = TTFont(fontfile)
#
#     matching = {}
#
#     for font in fonts:
#         glyphorder = ttfonts[font.BaseFont].getGlyphOrder()


def visitor_body(text, cm, tm, font_dict, font_size):
    global parts
    if font_dict is not None:
        if not text.isspace() and text != '\n' and text != '':
            parts.append((font_dict['/BaseFont'].split('/')[-1], text))


def gettext(pdf_path, mode='RusEng', startpage=0, endpage=0):
    # txt_path = __save_pdf_as_txt(pdf_path)
    # firstchars = get_encoding(txt_path)
    # charsOffonts = getCharsOfFonts(pdf_path)
    # print(charsOffonts)
    # font = TTFont("pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
    # print(font.getGlyphOrder(), charsOffonts['GRTMRT+TimesNewRomanPS-BoldMT'])
    global cnn
    cnn = CNN(mode)
    __extract_pfdfonts(pdf_path)
    __draw_glyphs()
    text = __gettextfrompdf(pdf_path, __match_glyphs_and_encoding_forall(mode), start=startpage, end=endpage)
    if mode == 'RusEng':
        text = correct_text(text)
    return text
