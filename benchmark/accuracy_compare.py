import json
import os

import requests
import glob
from Levenshtein import ratio
from icecream import ic

from pdf_worker.pdf_reader import PDFReader
from main import ROOT_DIR
from functions.functions import collapse_text, remove_hyphenations


def compare_two_strings_with_orig(cnn_string: str, tabby_string: str, orig: str):
    print(f"tabby: {ratio(orig, tabby_string)}, cnn: {ratio(orig, cnn_string)}")
    print(f"tabby text: {tabby_string}")
    print(f"cnn text: {cnn_string}")


def compare_dedoc_and_cnn(pdfs_path, txts_path, reader: PDFReader):
    data = {
        "pdf_with_text_layer": "false",
        "document_type": "other",
        "language": "rus+eng",
        "need_pdf_table_analysis": "true",
        "need_header_footer_analysis": "false",
        "is_one_column_document": "true",
        "return_format": 'plain_text',
        "structure_type": 'tree',
        'pages': '1:1'
    }

    pdfs = glob.glob(f"{pdfs_path}/*.pdf")
    txts = glob.glob(f'{txts_path}/*.json')

    pdf_names = [pdfname.split('\\')[-1].split('.')[0] for pdfname in pdfs]
    txt_names = [txtname.split('\\')[-1].split('.')[0] for txtname in txts]

    txts_and_pdfs = list(set(pdf_names).intersection(txt_names))

    for name in txts_and_pdfs:
        ic(name)

        txt_path = f'{txts_path}/{name}.json'
        pdf_path = f'{pdfs_path}/{name}.pdf'

        with open(txt_path, 'r', encoding='utf-8') as file:
            orig = json.load(file)

        start_page = orig['pages'][0]
        end_page = orig['pages'][1]
        data['pages'] = f"{start_page + 1}:{end_page}"

        with open(pdf_path, 'rb') as file:
            files = {'file': (pdf_path, file)}
            r = requests.post("http://localhost:1231/upload", files=files, data=data)
            result = r.content.decode('utf-8')
            tabby_text = ' '.join(result.split())

        cnn_text = reader.restore_text(pdf_path, start_page=start_page, end_page=end_page)
        compare_two_strings_with_orig(cnn_string=cnn_text, tabby_string=tabby_text, orig=orig['text'])
