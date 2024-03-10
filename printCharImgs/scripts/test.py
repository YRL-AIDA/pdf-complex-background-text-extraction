# from PyPDF2 import PdfReader
# from PyPDF2.generic import TextStringObject, NameObject, IndirectObject
#
# def extract_text_with_font(pdf_file_path):
#     text_with_font = []
#
#     with open(pdf_file_path, 'rb') as f:
#         pdf_reader = PdfReader(f)
#
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]
#             text = page.extract_text()
#             fonts_on_page = set()
#
#             try:
#                 resources = page['/Resources']
#                 if '/Font' in resources:
#                     fonts = resources['/Font']
#                     for font_obj in fonts.values():
#                         if isinstance(font_obj, IndirectObject):
#                             font_obj = font_obj.resolve()
#                         if '/BaseFont' in font_obj:
#                             font_name = font_obj['/BaseFont'].name
#                             fonts_on_page.add(font_name)
#             except KeyError:
#                 pass  # Handle if '/Resources' or '/Font' is not present in the page
#
#             text_with_font.append((text, fonts_on_page))
#
#     return text_with_font
#
# pdf_file_path = 'D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf'
# text_with_font = extract_text_with_font(pdf_file_path)
# for text, fonts in text_with_font:
#     print("Text:", text)
#     print("Fonts:", fonts)
from PyPDF2 import PdfReader
from pprint import pprint
import PyPDF2

def walk(obj, fnt, emb):
    '''
    If there is a key called 'BaseFont', that is a font that is used in the document.
    If there is a key called 'FontName' and another key in the same dictionary object
    that is called 'FontFilex' (where x is null, 2, or 3), then that fontname is
    embedded.

    We create and add to two sets, fnt = fonts used and emb = fonts embedded.
    '''
    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])
    if '/FontName' in obj:
        if [x for x in fontkeys if x in obj]:# test to see if there is FontFile
            emb.add(obj['/FontName'])

    for k in obj.keys():
        walk(obj[k], fnt, emb)

    return fnt, emb# return the sets for each page

if __name__ == '__main__':
    fname = 'D:\\rep\\fonts-recognition\\printCharImgs\\data\\checkpdf\\q.pdf'
    pdf = PdfReader(fname)
    fonts = set()
    embedded = set()
    for page in pdf.pages:
        obj = page.get_object()
        # updated via this answer:
        # https://stackoverflow.com/questions/60876103/use-pypdf2-to-detect-non-embedded-fonts-in-pdf-file-generated-by-google-docs/60895334#60895334
        # in order to handle lists inside objects. Thanks misingnoglic !
        # untested code since I don't have such a PDF to play with.
        if type(obj) == PyPDF2.generic.ArrayObject:  # You can also do ducktyping here
            for i in obj:
                if hasattr(i, 'keys'):
                    f, e = walk(i, fonts, embedded_fonts)
                    fonts = fonts.union(f)
                    embedded = embedded.union(e)
        else:
            f, e = walk(obj['/Resources'], fonts, embedded)
            fonts = fonts.union(f)
            embedded = embedded.union(e)

    unembedded = fonts - embedded
    print('Font List')
    pprint(sorted(list(fonts)))
    if unembedded:
        print ('\nUnembedded Fonts')
        pprint(unembedded)
