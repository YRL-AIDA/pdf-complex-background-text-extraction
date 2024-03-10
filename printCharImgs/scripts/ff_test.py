# from cnn_model import Model
# model = Model()
# model.prepare_data_fontforge()
import binascii

import PyPDF2
from Tools.scripts.fixcid import Char

# print(ord(''))
# s = r''
# for i in s:
#     print(Char.ConvertFromUtf32(i), i)
# print(binascii.hexlify(b'hello'))
# import gzip
# # compressed = b''
# with gzip.open('D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf') as f:
#     # print(123)
#     # fl = f.read()
#     # dec = gzip.decompress(fl)
#     print(f)
# arr = [438, 328, 597, 348, 328, 328, 358, 388, 368, 537, 358, 238, 408, 378, 507, 418, 338,
# 397, 398, 388, 378, 566, 537, 487, 289, 438, 348, 438, 378, 368, 467, 477, 457,
# 438, 418, 418, 477, 676, 488]
# print(len(arr))

from tika import parser

# raw = parser.from_file('D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf')
# raw = open('D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf', 'rb')
# print()
# # print()
# import PyPDF2
#
#
# def extract_text_from_pdf(pdf_path):
#     text = ''
#     with open(pdf_path, 'rb') as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         # for page_num in range(len(pdf_reader.pages)):
#         for page_num in range(1):
#             page = pdf_reader.pages[page_num]
#             text += page.extract_text()
#     return text
#
#
# pdf_path = 'D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf'
# extracted_text = extract_text_from_pdf(pdf_path)
#
# print(extracted_text)

# import fitz
# import chardet
# import codecs
#
# def custom_decode_text(text):
#     encoding = chardet.detect(text.encode())['encoding']
#     if encoding:
#         try:
#             decoded_text = text.encode('latin-1').decode(encoding)
#             return decoded_text
#         except Exception as e:
#             print(f"Error decoding text: {e}")
#     return None
#
# def extract_text_with_font_info(pdf_path):
#     fonts_info = {}
#     pdf_document = fitz.open(pdf_path)
#
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document[page_num]
#         for text_block in page.get_text("dict")["blocks"]:
#             for line in text_block["lines"]:
#                 for span in line["spans"]:
#                     font_info = (span["font"], span["size"])
#                     text = custom_decode_text(span["text"])
#                     if text:
#                         fonts_info[text] = font_info
#
#     return fonts_info
#
#
# font_text_info = extract_text_with_font_info(pdf_path)
#
# for text, (font_name, font_size) in font_text_info.items():
#     print(f"Text: {text}, Font Name: {font_name}, Font Size: {font_size}")

# from PyPDF2 import PdfReader
# from pprint import pprint
# import PyPDF2
#
# def walk(obj, fnt, emb):
#     '''
#     If there is a key called 'BaseFont', that is a font that is used in the document.
#     If there is a key called 'FontName' and another key in the same dictionary object
#     that is called 'FontFilex' (where x is null, 2, or 3), then that fontname is
#     embedded.
#
#     We create and add to two sets, fnt = fonts used and emb = fonts embedded.
#     '''
#     if not hasattr(obj, 'keys'):
#         return None, None
#     fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
#     if '/BaseFont' in obj:
#         fnt.add(obj['/BaseFont'])
#     if '/FontName' in obj:
#         if [x for x in fontkeys if x in obj]:# test to see if there is FontFile
#             emb.add(obj['/FontName'])
#
#     for k in obj.keys():
#         walk(obj[k], fnt, emb)
#
#     return fnt, emb# return the sets for each page
#
# if __name__ == '__main__':
#     fname = pdf_path
#     pdf = PdfReader(fname)
#     fonts = set()
#     embedded = set()
#     for page in pdf.pages:
#         obj = page.get_object()
#         # updated via this answer:
#         # https://stackoverflow.com/questions/60876103/use-pypdf2-to-detect-non-embedded-fonts-in-pdf-file-generated-by-google-docs/60895334#60895334
#         # in order to handle lists inside objects. Thanks misingnoglic !
#         # untested code since I don't have such a PDF to play with.
#         if type(obj) == PyPDF2.generic.ArrayObject:  # You can also do ducktyping here
#             for i in obj:
#                 if hasattr(i, 'keys'):
#                     f, e = walk(i, fonts)
#                     fonts = fonts.union(f)
#                     embedded = embedded.union(e)
#         else:
#             f, e = walk(obj['/Resources'], fonts, embedded)
#             fonts = fonts.union(f)
#             embedded = embedded.union(e)
#
#     unembedded = fonts - embedded
#     print('Font List')
#     pprint(sorted(list(fonts)))
#     if unembedded:
#         print ('\nUnembedded Fonts')
#         pprint(unembedded)

pdf_file_path = 'D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf'
from PyPDF2 import PdfReader
from PyPDF2.generic import TextStringObject, NameObject


def extract_text_with_font(pdf_file_path):
    text_with_font = []

    with open(pdf_file_path, 'rb') as f:
        pdf_reader = PdfReader(f)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            fonts_on_page = set()

            try:
                resources = page['/Resources']
                if '/Font' in resources:
                    fonts = resources['/Font']
                    for font in fonts.values():
                        if '/BaseFont' in font:
                            font_name = font['/BaseFont'].name
                            fonts_on_page.add(font_name)
            except KeyError:
                pass  # Handle if '/Resources' or '/Font' is not present in the page

            text_with_font.append((text, fonts_on_page))

    return text_with_font


text_with_font = extract_text_with_font(pdf_file_path)
for text, fonts in text_with_font:
    print("Text:", text)
    print("Fonts:", fonts)
