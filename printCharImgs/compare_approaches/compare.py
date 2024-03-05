import requests
import glob
from Levenshtein import ratio

from font_recognition import FontRecognizer

def compare_two_strings_with_orig(cnn_string: str, tabby_string: str, orig: str):
    print(f"tabby: {ratio(orig, tabby_string)}, cnn: {ratio(orig, cnn_string)}")
    print(f"tabby text: {tabby_string}")
    print(f"cnn text: {cnn_string}")


def evaluation_strings_loop(pdfs_path, txts_path, recognizer: FontRecognizer):
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
    txts = glob.glob(f'{txts_path}/*.txt')
    pdfnames = [pdfname.split('\\')[-1].split('.')[0] for pdfname in pdfs]
    txtnames = [txtname.split('\\')[-1].split('.')[0] for txtname in txts]
    txts_and_pdfs = list(set(pdfnames).intersection(txtnames))
    for name in txts_and_pdfs:
        print(name)
        # txt_path = f'../data/txts/{name}.txt'
        txt_path = f'{txts_path}/{name}.txt'
        # pdf_path = f'../data/pdf/{name}.pdf'
        pdf_path = f'{pdfs_path}/{name}.pdf'
        with open(pdf_path, 'rb') as file:
            files = {'file': (pdf_path, file)}
            r = requests.post("http://localhost:1231/upload", files=files, data=data)
            result = r.content.decode('utf-8')
            tabby_text = ' '.join(result.split())

        with open(txt_path, 'r', encoding='utf-8') as file:
            orig_text = file.read()

        cnn_text = recognizer.restore_text(pdf_path, end_page=1)
        compare_two_strings_with_orig(cnn_string=cnn_text, tabby_string=tabby_text, orig=orig_text)
