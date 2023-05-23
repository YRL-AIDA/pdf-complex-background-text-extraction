import fitz

import CNN_modelclass
import DataPrepare
import PDFData
from DataPrepare import generateimgs, generateAugedImgs, prepdata
from PDFData import gettext
from fontTools.ttLib import TTFont
import glob

from pathlib import Path
from typing import Iterable, Any
# from pdfminer.high_level import extract_pages

# from tensorflow import keras

# prepdata()

# print(ord("Á"))
# print(chr(193))

# restore_encoding("pdf/7.pdf")
# font = TTFont("pdfdata/extracted_font/TimesNewRoman,Bold.ttf")
# ffont = fitz.Font(fontfile="pdfdata/extracted_font/TimesNewRoman,Bold.ttf")
# print(chr(ffont.glyph_name_to_unicode(".notdef#22")))
# for i in font.getGlyphSet():
#     print(i)
# print("\N{Latin Capital Letter a with Acute}")
# print()
# print(b'\x00\x02\x00?\xff\xe4\x03\xb7\x05h\x00\x16\x00(\x00\xc0@\x1b\n\x03\x1a\x03*\x03\x03\x98\t\xa8\t\xb8\t\xc8\x0c\x04D\x08\x05\x17#\x05\x08\x17\x1f\'\x01\xbb\x01\x95\x00\x00\x00\x08\x01\x9a\xb3\'\'\x00\x1f\xb8\x01\n@\x0c\x0f\x05\x00\r\x17\xd1\x00\x19\x10\x19\x02\x19\xb8\x03\n@\x12\x13\x1a*#\xdc\x0b\xd1\x01@\x13\x154\x01\x19)\xf5\xf1\x18+N\x10\xf4+M\xf4\xedN\x10\xf6M\xfd]\xe4\x00??\xed\x129/\xed\x10\xed\x11\x129\x129\x01\x11\x12910Cy@2\x1a&\t\x12!%\r&\x11%\x1b\x1a\x1c\x1a\x1d\x1a\x03\x06%& \x0e#b\x00\x1e\x10\x19b\x01&\t#b\x00"\x0c\x1fb\x01\x1a\x12\x1fb\x01$\n\'b\x00\x00+++\x01++++*+++\x81\x81\x00]\x01]\x175>\x027\x06\x06#"&546632\x16\x12\x15\x14\x02\x04\x01654\'&\'&#"\x07\x06\x15\x10\x17\x1632?\xa6\xe7\x87\x1b>W0\x9a\xcdo\xceow\xd4~\xcd\xfej\x01)\n*\x18/\x19(2\x1c\'B+I\'\x1c\x1c&\x94\xda\x8e \x19\xde\xc1\x86\xdf{\x88\xfe\xfe\xa5\xd6\xfex\xed\x02\x88pU\xb6\x9dW)\x16+;\xa6\xfe\xebiD\x00'.decode("UTF-32"))
# print(','.encode())
# print(list(one))
# print(ord('1'))
# print(list(x))
# print(x.decode('utf-32'))
# bytes_data = []
# t = ""
# for i in x:
#     t += chr(i)
#     bytes_data.append(i)
# print(t)
# print("".join(map(chr, bytes_data)))
# q = font.getGlyphSet().glyfTable.glyphs['quotedbl'].data
# print(q.decode('UTF-8'))
#
# import fitz
# dictionary = restore_encoding(pdf_path="pdf/7.pdf")
# print(dictionary)
# doc = fitz.open("pdf/7.PDF")
# for page in doc:
#     for i in page.get_text("dict")['blocks']:
#         for j in i['lines']:
#             for k in j['spans']:
#                 font = TTFont("pdfdata/extracted_font/" + k['font'] + ".ttf")
#                 cmap = font.getBestCmap()
#                 s2 = ""
#                 for index, char in enumerate(k['text']):
#                     try:
#                         # print(dictionary[k['font']][char])
#                         s2 += dictionary[k['font']][char]
#                     except KeyError:
#                         s2 += char
#                 print(s2)
#     break
# prepdata()
# print(__file__)
# gettext("pdf/7.PDF")
# CNN_modelclass.recognize_glyph("pdfdata/glyphimages/TimesET,Italic/Agrave.png")
doc = fitz.open("pdf/7.PDF")
print(doc)