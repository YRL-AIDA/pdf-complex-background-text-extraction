import glob
# -*- coding: utf-8 -*-
import requests
from icecream import ic

from font_recognition import FontRecognizer

data = {
    "document_type": "other",
    "language": "rus+eng",
    "need_pdf_table_analysis": "true",
    "need_header_footer_analysis": "false",
    "is_one_column_document": "false",
    "return_format": 'plain_text',
    "structure_type": 'tree',
    'pages': '1:1',
    'pdf_with_text_layer': 'false'
}

q = "../data/checkpdf2"
qq = "../data/checkpdf"
qqq = "../data/check_pdf"
norm = ['154', '278.json', 'hz', 'hz2', 'hz3']
pdf = f'{qqq}/3.pdf'
with open(pdf, 'rb') as file:
    ic(f'pdf name: {pdf}')
    files = {'file': (pdf, file)}
    r = requests.post("http://localhost:1231/upload", files=files, data=data)
    result = r.content.decode('utf-8')
    dedoc_text = ' '.join(result.split())
    ic(dedoc_text)

#lntegratable isolation system Available for SLNA Workstation on request Safe processing of unknown lmmediate benefits external data sources Process unsecure websites, usb sticks or files at аnу time Comfortable and unrestricted internet access for all users Professional solution for poorly manageable internet PCs, virtual desktops, thin client sessions or other individual solutions Еаsу integration in the SLNA Workstation Vегу high level of automation Default browser appearance Right of use already included in every new SLNA Workstation Client versions also available for systems without SLNA Quarantine system for сомрlех administration structures ГЕсОВS Bitbox Contamination system DMZ-in-a-box system lnternet  safe surfer concentrator safe surfer "Quarantine system" Central lnternal Win  (VS guest) safe surfer "Quarantine system" safe surfer "Quarantine system" Windows  SLNA Workstation mobile client Thin/Fat client Would you like to learn more? Воок а webinar here or request а non-committal and free trial installation. Contact us here secunet.com/safesurfer secunet ist Sicherheitspartner der Bundesrepublik Deutschland secunet is а security partner of the German Federal Government and а member of all relevant industry associations.
