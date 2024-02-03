from cnn_model import Model
from font_recognition import FontRecognizer
from config import DefaultModel
#
fr_rus_eng = FontRecognizer.create_with_default_mode(DefaultModel.Russian_and_English)
# fr_rus = FontRecognizer.c reate_with_default_mode(DefaultModel.Russian)
# # fr_eng = FontRecognizer.create_with_default_mode(DefaultModel.English)
# #
# # # frs = [fr_rus_eng, fr_rus, fr_eng]
# #
p = "../data/pdf/"
paths = [p + "1.pdf", p + "2.pdf", p + "3.pdf", p + "4.pdf"]
# # fr_rus_eng.restore_text("../data/pdf/1.pdf")
# # # fr_rus_eng.print_text()
# #
fr_rus_eng.restore_text(paths[2])
# fr_rus_eng.print_text()

from fontTools import t1Lib
# f = fontforge.open("../data/pdfdata/extracted_fonts/ANTQUAI.pfa")
# doc = t1Lib.T1Font(path="../data/pdfdata/extracted_fonts/IMXRQI+CMR8.pfa")
# doc = t1Lib.T1Font(path="../data/pdfdata/extracted_fonts/ANTQUAI.pfa")


import fitz
# doc = fitz.open(paths[3])

# print(doc[4].get_text("text"))
# for blocks in doc[4].get_text("dict")['blocks']:
#     print(blocks)
#     print()

# sent = ""
# for blocks in doc[4].get_text("dict")['blocks']:
#     print("new block")
#     for lines in blocks['lines']:
#         print("new line")
#         line_text = ""
#         for spans in lines['spans']:
#             # print("new span")
#             word = ""
#             for index, char in enumerate(spans['text']):
#                 word += char
#             # print(word)
#             line_text += word
#         line_text = line_text.lstrip(' ')
#         sent += line_text
#     print(sent)
#         # sentence += line_text
#         # sentence += "\n"


# from pdfreader import PDFDocument
# fd = open("../data/pdf/4.pdf", 'rb')
# doc = PDFDocument(fd)
# page = next(doc.pages())
# sorted(page.Resources.Font.keys())
# font = page.Resources.Font[page.Resources.Font.keys()[0]]
# print(font.Subtype,"|", font.BaseFont,"|", font.Encoding)


# def _decryptChar(cipher, R):
#     cipher = byteord(cipher)
#     plain = ((cipher ^ (R >> 8))) & 0xFF
#     R = ((cipher + R) * 52845 + 22719) & 0xFFFF
#     return bytechr(plain), R
#
#
# def _encryptChar(plain, R):
#     plain = byteord(plain)
#     cipher = ((plain ^ (R >> 8))) & 0xFF
#     R = ((cipher + R) * 52845 + 22719) & 0xFFFF
#     return bytechr(cipher), R
#
#
# def decrypt(cipherstring, R):
#     plainList = []
#     for cipher in cipherstring:
#         plain, R = _decryptChar(cipher, R)
#         plainList.append(plain)
#     plainstring = bytesjoin(plainList)
#     return plainstring, int(R)
