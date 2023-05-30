import glob
import shutil

# from PDFData import gettext
from Analize import analize_word
from fontTools.ttLib import TTFont
import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer,  LTChar
from pathlib import Path
from fitz import adobe_glyph_names
from PIL import ImageFont

from fontTools.agl import toUnicode
# !
# text = gettext("pdf/10.PDF")
# # print(ord(toUnicode('uni
# 041A')) - ord('!'))
# # print(ord(toUnicode('uni041C')) - ord('"'))
# print(ord(toUnicode('uni041A')), ord('!'))
# print(ord(toUnicode('uni041C')), ord('"'))
# print(ord(toUnicode('uni041E')), ord('#'))
# print(text)

# text = gettext("pdf/10.PDF")
# font = fitz.Font("pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
# print(adobe_glyph_names())
# print(font.g)
# import DrawGlyph
# q = ImageFont.truetype(font="pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
# DrawGlyph.drawglyph_pillow(q, "$", (28, 28)).show()
# gettext("pdf/7.PDF")
from fontTools.afmLib import AFM
# afm = AFM("pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
from PDFData import gettext

# font = TTFont("pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
# font = TTFont("pdfdata/extracted_font/VGPRFL+TimesNewRoman,Bold.ttf")
# font['cmap']
# font['cmap']
# for i,j in zip(font['cmap'].tables[0].cmap, font['cmap'].tables[0].cmap.values()):
#     print(i,j)
# font['cmap']
# print(font.getBestCmap())
# print(font.getGlyphNames())
# print(font.getGlyphOrder())
from pdfreader import PDFDocument, SimplePDFViewer

fd = open("pdf/11.pdf", "rb")
doc = PDFDocument(fd)
from itertools import islice
# fonts = {}
# for page in doc.pages():
#     # print(page.Resources.Font)
#     for i, j in zip(page.Resources.Font, page.Resources.Font.values()):
#         fonts[i] = j



# fontfiles = glob.glob("pdfdata/extracted_font/*.ttf")
# ttfonts = {}
# for fontfile in fontfiles:
#     ttfonts[fontfile.split('\\')[-1].split('.')[0]] = TTFont(fontfile)


# ff = fitz.Font(fontfile="pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
# # print(ff.valid_codepoints())
# for i in ff.valid_codepoints():
#     print(chr(i))
# for font in fonts.values():
#     glyphorder = ttfonts[font.BaseFont].getGlyphOrder()
#     # print(font.BaseFont)
#     # print(glyphorder)
#     # print(ttfonts[font.BaseFont].getGlyphNames())
#     firstchar = font.FirstChar
#     lastchar = font.LastChar
#     # convdict = {toUnicode(x): chr(y) for x, y in zip(glyphorder, range(33, 33 + len(glyphorder)))}
#
#     glyphorder = [toUnicode(x) for x in glyphorder]


# cmap = {}
# for page in doc.pages():
#     print(page)
# viewer = SimplePDFViewer(fd)
# viewer.render()
# md = viewer.canvas.strings
# print(md)
#     cmap = {fontname: fontcmap for fontname, fontcmap in zip(fontinfo.BaseFont, fontinfo.Type for fontinfo in page.Resources.Font)}
# cmaps = {x: y for x, y in zip(f,f for f in z.Resources.Font.values for z in pages)}

# qwer = {x: y for x, y in zip(fonts.)}
# for font in fonts:


# page = next(islice(doc.pages(), 0, 1))
# # print(page)
# f = page.Resources.Font['F3.1']
# # dd = {x: y for x, y in zip(fonts.keys(), next(islice(doc.pages(), 0)))}
# # print(list(islice(doc.pages(), 0, None)))
# # for i in list(islice(doc.pages(), 0, None)):
# #     print(i)
# # print(list(islice('ABCDEFG', 0, None, 1)))
# # print(fonts)
# cmap = f.ToUnicode
# data = cmap.filtered
# print(data.decode())
# print(ord(toUnicode('u003A')))
# print(ord(toUnicode('u041A')) - ord(toUnicode('u0021')))
# print(toUnicode('u0005'))

text = gettext("pdf/11.pdf")
for i in text:
    print(i)


# import PDFData
# print(PDFData.recognize_glyph("pdfdata/glyphimages/OVZFUR+TimesNewRomanPSMT/).png"))