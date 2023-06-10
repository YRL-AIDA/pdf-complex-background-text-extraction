import glob
import shutil

# from PDFData import gettext
from PyPDF2 import PdfReader, PdfFileReader
from pdfreader import PDFDocument, SimplePDFViewer

from Analize import analize_word
from fontTools.ttLib import TTFont
import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer,  LTChar
from pathlib import Path
from fitz import adobe_glyph_names
from PIL import ImageFont

from fontTools.agl import toUnicode
from DataPrepare import prepdata
from PDFData import gettext
import PDFData
import sys
sys.path.insert(0, 'testqual')
from text_evaluation import similarity
import re
# doc = fitz.open("pdf/11.pdf")
# for page in doc:
#     print(page.number)
#     for i in page.get_text('rawdict')['blocks']:
#         print(i)

doc = PDFDocument(open('pdf/11.pdf', 'rb'))
viewer = SimplePDFViewer(open('pdf/11.pdf', 'rb'))
# for canvas in viewer:
#     pass
#     print(canvas.strings)
# for page in doc.pages():
#     print(page.Resources.ProcSet[1])

reader = PdfReader("pdf/7.pdf")

page = reader.pages[0]

parts = []


def visitor_body(text, cm, tm, font_dict, font_size):
    # print(text)
    # parts.append(text)
    print(text, cm, tm, font_dict)
    # if font_dict is not None:
    #     parts.append(text)

# for page in reader.pages:
#     text = page.extract_text()
#     for line in text:
#         print(line)
# doc = fitz.open('pdf/7.PDF')
# p = doc[0]
    # text_lower = text.lower()
    # for line in text_lower:
    #     print(line)
# page.extract_text(visitor_text=visitor_body)
# page.extract_text(visitor_text=visitor_body)
# text_body = " ".join(parts)
# print(text_body)
# text_body = "".join(parts)
# for i in reader.pages:
#     i.extract_text(visitor_text=visitor_body)
# text_body = ""
# for i in parts:
#     # print("")
#     text_body += i[1]
# print(text_body)



with open('testqual/ex.txt', 'r', encoding='utf-8') as file:
    extracted = file.read().replace('\n', '')
    extracted = re.sub(' +', ' ', extracted)

with open('testqual/or.txt', 'r', encoding='utf-8') as file:
    orig = file.read().replace('\n', '')
    orig = re.sub(' +', ' ', orig)


print(similarity(extracted, orig))

# print(PDFData.__gettextfrompdf("pdf/2.pdf", {}))

text = gettext("pdf/7.pdf", mode='Rus', endpage=2)
for i in text:
    print(i)

