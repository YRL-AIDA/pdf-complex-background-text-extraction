import shutil

from PDFData import gettext
from Analize import analize_word
from fontTools.ttLib import TTFont
import fitz
# from pdfquery import PDFQuery
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer,  LTChar
from pathlib import Path

from fontTools.agl import toUnicode

text = gettext("pdf/10.PDF")
# print(text)
# font = TTFont("pdfdata/extracted_font/OPEHOG+TimesET,Italic.ttf")
# Ò
# print(font.getGlyphName('Ò'))
# print(font.getGlyphOrder())
# for i in font.getGlyphName('Ò')

# print("1")
# 'uni0412'
# hex(sys.maxunicode)
# '0xffff'
# snake = tuple(codepoints.from_unicode(u'\U0001F40D'))
# print(len(snake))
# print(snake[0])
# print(hex(snake[0]))
# '0x1f40d'
# font = TTFont("pdfdata/extracted_font/GRTMRT+TimesNewRomanPS-BoldMT.ttf")
#
# f = fitz.Font(fontfile="pdfdata/extracted_font/BHSASO+TimesNewRomanPSMT.ttf")
# vuc = f.valid_codepoints()
# for i in vuc:
#     print(chr(i))

import fitz
# from collections import OrderedDict
# dict = {}
# text = ""
# for page_layout in extract_pages("pdf/10.pdf"):
#     for element in page_layout:
#         if isinstance(element, LTTextContainer):
#             # print(element.get_text())
#             text = element.get_text()
#             # print(text)
#             for text_line in element:
#                 try:
#                     for char in text_line:
#                         try:
#                          if isinstance(char, LTChar):
#                             # "123"
#                             text = text.replace(' ', '')
#                             text = text.replace('\n', '')
#                             if char.fontname not in dict.keys():
#                                 dict[char.fontname] = list(OrderedDict.fromkeys(text))
#                             else:
#                                 dict[char.fontname] = dict[char.fontname] + list(OrderedDict.fromkeys(text))
#                             # print(dict[char.fontname] + [x for x in text])
#                             break
#                         except:
#                             pass
#                 except:
#                     pass
# print(dict['GRTMRT+TimesNewRomanPS-BoldMT'])

# print(chr(33))
