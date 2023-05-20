import CNN_modelclass
import DataPrepare
import PDFData
from DataPrepare import generateimgs, generateAugedImgs, prepdata
from PDFData import restore_encoding
# from CNN_modelclass import recognize_glyph
from fontTools.ttLib import TTFont
import glob

# from tensorflow import keras

prepdata()
# restore_encoding(pdf_path="pdf/2.pdf")
# print(CNN_modelclass.recognize_glyph("imgs/trainimgs/Rus_hard/Rus_hard_24.png"))
# recognize_glyph("pdfdata/glyphimages/ELFODM+TimesNewRomanPSMT.ttf/8.png")
# recognize_glyph("imgs/trainimgs/p/p_lower_0.png")

# f = TTFont("pdfdata/extracted_font/ELFOEN+TimesNewRomanPS-BoldMT.ttf")
# f = TTFont("fonts/fontstrain/AACH.TTF")
# print(f['cmap'].getBestCmap().items())
# print(f['cmap'].getBestCmap())
# f['cmap'] = {65 : 'A'}
# print(f['cmap'])
# print(chr(33))

# f = TTFont("fonts/fontstrain/AACH.TTF")
# print(f.getBestCmap())

# q = glob.glob("imgs/trainimgs/Rus_h/*")
# for i in q:
#     print(CNN_modelclass.recognize_glyph(i))

