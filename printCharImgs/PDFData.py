import configparser
import glob
import os
import shutil
from copy import copy

import fitz
from PIL import ImageFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

from CNN_modelclass import recognize_glyph
from DrawGlyph import drawglyph_by_pen, drawglyph_pillow

config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')
# config.read('config.ini', encoding='utf-8')

invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
inv_map = {v: k for k, v in invalid_symbols.items()}
invalid_symbolsnoregdiff = eval(config.get("DEFAULT", "invalidSymbolsnoregdiff"))
inv_mapnoregdiff = {v: k for k, v in invalid_symbolsnoregdiff.items()}


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
        # pfont = fitz.Font(fonts_path + "/" + fontname)
        tosavefolder = fontname.split('.')[0]
        f1 = ImageFont.truetype(fonts_path + "/" + fontname, 18)
        # font = ttLib.SFNTReader(fonts_path + "/" + fontname)
        # font = fontTools.cffLib.CFFFontSet.convertCFFToCFF2(fonts_path + "/" + fontname)
        os.makedirs(save_path + "/" + tosavefolder)
        glyphset = font.getGlyphSet()
        size = 0
        minsize = 10000
        # size = 0, 0
        for g in glyphset:
            bp = BoundsPen(glyphset)
            glyph = glyphset[g]
            glyph.draw(bp)
            if bp.bounds is None:
                continue

            # ranshe size bil tolko dly height menya tut i v drawglyph_by_pen
            # if bp.bounds[1] < 0:
            #     size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            #     minsize = min(minsize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            minsize = min(minsize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
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
            img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, minsize=minsize)
            # img = drawglyph_pillow(pfont, pfont.glyph_name_to_unicode(g), (28, 28))
            if img is None:
                continue
            if g[0] == '.':
                g = g.replace('.', "")
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
            # name = font['name']
            name = font['name'].split("+", 1)[1] if "+" in font['name'] else font['name']
            if font['ext'] != "n/a":
                ofile = open(dir + name + "." + font['ext'], "wb")
                # print(dir + font['name'] + "." + font['ext'])
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
                doc[page_num].insert_font(fontname="VGPRFL+TimesNewRoman,Bold", fontfile="pdfdata/extracted_font/VGPRFL+TimesNewRoman,Bold.ttf")
            if font['name'] == 'ATSFPL+TimesNewRoman,BoldItalic':
                print("123")
                doc[page_num].insert_font(fontname="ATSFPL+TimesNewRoman,BoldItalic", fontfile="pdfdata/extracted_font/ATSFPL+TimesNewRoman,BoldItalic.ttf")
            if font['name'] == 'FCDHEK+TimesNewRoman,Italic':
                print("123")
                doc[page_num].insert_font(fontname="FCDHEK+TimesNewRoman,Italic", fontfile="pdfdata/extracted_font/FCDHEK+TimesNewRoman,Italic.ttf")
            if font['name'] == 'MVVIUJ+TimesNewRoman':
                print("123")
                doc[page_num].insert_font(fontname="MVVIUJ+TimesNewRoman", fontfile="pdfdata/extracted_font/MVVIUJ+TimesNewRoman.ttf")
            if font['name'] == 'OPEHOG+TimesET,Italic':
                print("123")
                doc[page_num].insert_font(fontname="OPEHOG+TimesET,Italic", fontfile="pdfdata/extracted_font/OPEHOG+TimesET,Italic.ttf")
    doc.save("123.pdf")
    doc.close()


def __match_glyphs_and_encoding(ttffont, fitzfont, images):
    images = glob.glob(images + "/*")
    # ne vidit .notdef (.)
    dict = {}
    cmap14 = CmapSubtable.newSubtable(14)
    # cmap = ttffont.getBestCmap()
    # inv_cmap = {v: k for k, v in cmap.items()}
    # gs = ttffont.getGlyphSet()
    # inv_cmap = {i: fitzfont.glyph_name_to_unicode(i) for i in gs.items()}
    inv_cmap = {i: fitzfont.glyph_name_to_unicode(i) for i in ttffont.getGlyphNames()}
    # print(cmap)
    for img in images:
        # if pred in inv_map:
        #     key = ord(inv_map[pred])
        #     # key = (img.split('\\')[-1]).split('.')[0]
        # else:
        #     key = ord(pred)
        #     # key = ord(pred)
        # name = img.split('\\')[-1]
        # name = name.split('.')[0]
        # dict[name] = key

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
        dicts[fontnameimgs] = __match_glyphs_and_encoding(ttffont, fitzfont, imgfolders + fontnameimgs)
    return dicts


def __gettextfrompdf(pdf_path, dictionary):
    print(dictionary)
    doc = fitz.open(pdf_path)
    s2 = ""
    text = []
    for page in doc:
        s2 = ""
        for i in page.get_text("dict")['blocks']:
            try:
                for j in i['lines']:
                    for k in j['spans']:
                        # s2 = ""
                        for index, char in enumerate(k['text']):
                            try:
                                s2 += dictionary[k['font']][char]
                                # s2 += '[' + char + ']'
                            except KeyError:
                                s2 += char
                        # print(s2)
                    s2 += "\n"
            except:
                pass
        text.append(s2)
        # break
    print(s2)
    return text


def gettext(pdf_path):
    __extract_pfdfonts(pdf_path)
    __draw_glyphs()
    return __gettextfrompdf(pdf_path, __match_glyphs_and_encoding_forall())


# def __draw_glyphs(save_path="pdfdata/glyphimages", fonts_path="pdfdata/extracted_font"):
#     save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
#     fonts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fonts_path)
#     if os.path.isdir(save_path):
#         shutil.rmtree(save_path)
#     os.makedirs(save_path)
#     font_files = os.listdir(os.fsencode(fonts_path))
#     counter = 0
#     for font_file in font_files:
#         fontname = os.fsdecode(font_file)
#         font = TTFont(fonts_path + "/" + fontname)
#         tosavefolder = fontname.split('.')[0]
#         f1 = ImageFont.truetype(fonts_path + "/" + fontname, 18)
#         # font = ttLib.SFNTReader(fonts_path + "/" + fontname)
#         # font = fontTools.cffLib.CFFFontSet.convertCFFToCFF2(fonts_path + "/" + fontname)
#         os.makedirs(save_path + "/" + tosavefolder)
#         glyphset = font.getGlyphSet()
#         size = 0
#         minsize = 10000
#         # size = 0, 0
#         for g in glyphset:
#             bp = BoundsPen(glyphset)
#             glyph = glyphset[g]
#             glyph.draw(bp)
#             if bp.bounds is None:
#                 continue
#
#             # ranshe size bil tolko dly height menya tut i v drawglyph_by_pen
#             if bp.bounds[1] < 0:
#                 # size = max(size[0], abs(bp.bounds[0]) + abs(bp.bounds[2])), \
#                 #        max(size[1], abs(bp.bounds[1]) + abs(bp.bounds[3]))
#                 size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
#                 minsize = min(minsize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
#         for g in glyphset:
#
#             ## method mb nado raskomentit budet tak chto poka tak
#
#             # pen = FreeTypePen(glyphset)
#             # bp = BoundsPen(glyphset)
#             # glyph = glyphset[g]
#             # glyph.draw(pen)
#             # glyph.draw(bp)
#             # if bp.bounds is None:
#             #     continue
#             # # img = pen.image(width=glyph.width, height=abs(bp.bounds[1] + bp.bounds[3]), contain=True)
#             # if bp.bounds[1] > 0:
#             #     img = pen.image(width=glyph.width, height=(bp.bounds[1] + bp.bounds[3])/2, contain=True)
#             # else:
#             #     # img = pen.image(width=glyph.width, height=1300, contain=True)
#             #     img = pen.image(width=glyph.width, height=size, contain=True)
#             #     # img = pen.image(width=glyph.width, height= (abs(bp.bounds[1]) + abs(bp.bounds[3]))+500, contain=True)
#             # # img = pen.image(width=abs(bp.bounds[0] + bp.bounds[2]), height=abs(bp.bounds[1] + bp.bounds[3])*2)
#             # # img = pen.image(width=glyph.width, height=abs(bp.bounds[1] + bp.bounds[3]), contain=True)
#             # background = Image.new('LA', img.size, (255, 255))
#             # alpha_composite = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
#             # alpha_composite = alpha_composite.convert("L")
#             # # alpha_composite = alpha_composite.resize((20, 20))
#             # alpha_composite.thumbnail((28, 28))
#             # alpha_composite = ImageOps.invert(alpha_composite)
#             # # alpha_composite = alpha_composite.resize((20, 20))
#             # img = alpha_composite
#             # new_im = Image.new("L", (28, 28))
#             # box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
#             # new_im.paste(img, box)
#             # img = new_im
#             # img.save(save_path + "/" + fontname + "/" + str(counter) + ".png")
#
#             ## method
#             img = drawglyph_by_pen(ttfont=font, glyph_name=g, size=size, minsize=minsize)
#
#             if img is None:
#                 continue
#             if g[0] == '.':
#                 g = g.replace('.', "")
#             pngname = g + "_lower" if g.islower() else g + "_upper" if g.isupper() else g
#             img.save(save_path + "/" + tosavefolder + "/" + pngname + ".png")
#             counter += 1
#
#
# def __extract_pfdfonts(pdf, save_path="pdfdata/extracted_font"):
#     save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
#     if os.path.isdir(save_path):
#         shutil.rmtree(save_path)
#     os.makedirs(save_path)
#     doc = pdf
#     xref_visited = []
#     dir = save_path + "/"
#     if os.path.exists(dir):
#         shutil.rmtree(dir)
#     os.mkdir(dir)
#     for page_num in range(doc.page_count):
#         page = doc.get_page_fonts(page_num)
#         for fontinfo in page:
#             xref = fontinfo[0]
#             if xref in xref_visited:
#                 continue
#             xref_visited.append(xref)
#             font = doc.extract_font(xref, named=True)
#             # name = font['name']
#             name = font['name'].split("+", 1)[1] if "+" in font['name'] else font['name']
#             if font['ext'] != "n/a":
#                 ofile = open(dir + name + "." + font['ext'], "wb")
#                 # print(dir + font['name'] + "." + font['ext'])
#                 ofile.write(font['content'])
#                 ofile.close()
#     doc.close()
#
#
# def __match_glyphs_and_encoding(ttffont, fitzfont, images):
#     images = glob.glob(images + "/*")
#     # ne vidit .notdef (.)
#     dict = {}
#     cmap14 = CmapSubtable.newSubtable(14)
#     cmap = ttffont.getBestCmap()
#     inv_cmap = {v: k for k, v in cmap.items()}
#     # gs = ttffont.getGlyphSet()
#     # inv_cmap = {i: fitzfont.glyph_name_to_unicode(i) for i in gs.items()}
#     inv_cmap = {i: fitzfont.glyph_name_to_unicode(i) for i in ttffont.getGlyphNames()}
#     # print(cmap)
#     for img in images:
#         # if pred in inv_map:
#         #     key = ord(inv_map[pred])
#         #     # key = (img.split('\\')[-1]).split('.')[0]
#         # else:
#         #     key = ord(pred)
#         #     # key = ord(pred)
#         # name = img.split('\\')[-1]
#         # name = name.split('.')[0]
#         # dict[name] = key
#
#         key = ((img.split('\\')[-1]).split('.')[0]).split('_')[0]
#         if key not in inv_cmap:
#             continue
#         pred = recognize_glyph(img)
#         key = chr(inv_cmap[key])
#         # print(key)
#         # if pred in inv_map:
#         #     name = inv_map[pred]
#         if pred in inv_mapnoregdiff:
#             name = inv_mapnoregdiff[pred]
#         else:
#             name = pred
#         dict[key] = name
#     # cmap14.platformID = 3
#     # cmap14.platEncID = 10
#     # # cmap14.language = 0
#     # cmap14.cmap = dict
#     # cmap = newTable("cmap")
#     # cmap.tableVersion = 0
#     # cmap.tables = [cmap14]
#     # font['cmap'] = cmap
#     # print(font.getBestCmap())
#     # return font.getBestCmap()
#     return dict
#
#
# def __match_glyphs_and_encoding_forall():
#     imgfolders = "pdfdata/glyphimages/"
#     imgfolders = os.path.join(os.path.dirname(os.path.abspath(__file__)), imgfolders)
#     extracted_fonts_folder = "pdfdata/extracted_font/*"
#     extracted_fonts_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), extracted_fonts_folder)
#     fonts = glob.glob(extracted_fonts_folder)
#     dicts = {}
#     for fontfile in fonts:
#         fontname = fontfile.split('\\')[-1]
#         ttffont = TTFont(fontfile)
#         fitzfont = fitz.Font(fontfile=fontfile)
#         fontnameimgs = fontname.split('.')[0]
#         dicts[fontnameimgs] = __match_glyphs_and_encoding(ttffont, fitzfont, imgfolders + fontnameimgs)
#     return dicts
#
#
# def __gettextfrompdf(pdf, dictionary):
#     print(dictionary)
#     s2 = ""
#     for page in pdf:
#         for i in page.get_text("dict")['blocks']:
#             for j in i['lines']:
#                 for k in j['spans']:
#                     # s2 = ""
#                     for index, char in enumerate(k['text']):
#                         try:
#                             s2 += dictionary[k['font']][char]
#                         except KeyError:
#                             s2 += char
#                     # print(s2)
#         break
#     return s2
#
#
# def gettext(pdf):
#     qq = copy(pdf)
#     __extract_pfdfonts(qq)
#     __draw_glyphs()
#     __gettextfrompdf(qq, __match_glyphs_and_encoding_forall())