import glob
import os
from Levenshtein import ratio
import requests
from pathlib import Path
from font_recognition import FontRecognizer
from compare_approaches import compare

#
# data = {
#     "pdf_with_text_layer": "false",
#     "document_type": "other",
#     "language": "rus+eng",
#     "need_pdf_table_analysis": "true",
#     "need_header_footer_analysis": "false",
#     "is_one_column_document": "true",
#     "return_format": 'plain_text',
#     "structure_type": 'tree',
#     'pages': '1:1'
# }
#
# pdfs_path = "../data/pdf"
# pdfs_dir = os.fsencode(pdfs_path)
# pdfs = glob.glob("../data/pdf/*.pdf")
# txts = glob.glob("../data/txts/*.txt")
# model_re = Model.load_default_model()
# fr_re = FontRecognizer.load_default_model()
#
# t1 = "Как познакомиться с помощью Шаблона Стагнера?"
# t2 = "1 кaк пoзнaкoмиться с пoмoщью шaблoнa стaгнeрa?"
# t3 = "Как познакомиться с помощью Шаблона Стагнера?"
# # print(f"tabby: {ratio(t1, t3)}, cnn: {ratio(t1, t2)}")
#
# pdfnames = [pdfname.split('\\')[-1].split('.')[0] for pdfname in pdfs]
# txtnames = [txtname.split('\\')[-1].split('.')[0] for txtname in txts]
# # pdfnames = [pdfname for pdfname in ]
# txts_and_pdfs = list(set(pdfnames).intersection(txtnames))
# # for (pdf, txt) in zip(pdfs, txts):
# #     print(pdf, txt)
# #
# #     with open(pdf, 'rb') as file:
# #         files = {'file': (pdf, file)}
# #         r = requests.post("http://localhost:1231/upload", files=files, data=data)
# #         result = r.content.decode('utf-8')
# #         # print(' '.join(result.split()))
# #         tabby_text = ' '.join(result.split())
# #
# #     with open(txt, 'r', encoding='utf-8') as file:
# #         orig_text = file.read()
# #
# #     cnn_text = fr_re.restore_text(pdf)
# #
# #     print(pdf.split('\\')[-1])
# #     print(f"tabby: {ratio(orig_text, tabby_text)}, cnn: {ratio(orig_text, cnn_text)}")
# #     print(f"cnn text: {cnn_text}")
# #     print(f"tabby text: {tabby_text}")
# # # tabby: 0.986793349168646, cnn: 0.7447191436961258
# #     break
# # print(chr(63))
#
#
# for name in txts_and_pdfs:
#     print(name)
#     txt_path = f'../data/txts/{name}.txt'
#     pdf_path = f'../data/pdf/{name}.pdf'
#     with open(pdf_path, 'rb') as file:
#         files = {'file': (pdf_path, file)}
#         r = requests.post("http://localhost:1231/upload", files=files, data=data)
#         result = r.content.decode('utf-8')
#         # print(' '.join(result.split()))
#         tabby_text = ' '.join(result.split())
#
#     with open(txt_path, 'r', encoding='utf-8') as file:
#         orig_text = file.read()
#
#     cnn_text = fr_re.restore_text(pdf_path, end_page=1)
#
#     print(f"tabby: {ratio(orig_text, tabby_text)}, cnn: {ratio(orig_text, cnn_text)}")
#     print(f"cnn text: {cnn_text}")
#     print(f"tabby text: {tabby_text}")
#     # break

q = "../data/checkpdf2"
qq = "../data/checkpdf"
norm = ['154', '278.json', '767']
p = "../data/checkpdf2/q.pdf"
tabby_text = 'Australasian Information Evaluation Program | | Report Junos OS 20. 2R1 for SRX345, И SRX345- DUAL- AC, SRX380 and: SR X1500 О Nersion 1:6, 03 December Ам. > = РЕ чиччиче -- > до мч. - > ААчАШФеллд = ‹ ‹ о - - - - ФА..--.--- eee и чо ч esr BOP > р < Ш} > > ACP > ee | | < < YO © Ир or acer hr rh mh wr Br aA > mr ДА > OdOP чь © АЩЬ ee ee >> > ор rca COAAAP sr Adi но + > чочь <> erra maa aap eon «Ш Ar > Ар < > <r с Бег. ома dP у 9 и ДА > = <> ss дор <> и ор 4 4» › «cc. ччор <'
recognizer = FontRecognizer.load_default_model()
cnn_text = recognizer.restore_text_fontforge(f'{q}/{norm[-1]}.pdf', start_page=0, end_page=1)
orig = 'Australasian Information Security Evaluation Program  Certification Report Juniper Junos OS 20.2R1 for SRX345, SRX345-DUAL-AC, SRX380 and SRX1500 Version 1.0, 03 December 2020'
compare.compare_two_strings_with_orig(cnn_text, tabby_text, orig)

