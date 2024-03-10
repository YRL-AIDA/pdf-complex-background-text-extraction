from pathlib import Path
from typing import Iterable, Any

from pdfminer.high_level import extract_pages


def show_ltitem_hierarchy(o: Any, depth=0):
    """Show location and text of LTItem and all its descendants"""
    if depth == 0:
        print('element                        fontname             text')
        print('------------------------------ -------------------- -----')

    print(
        f'{get_indented_name(o, depth):<30.30s} '
        f'{get_optional_fontinfo(o):<20.20s} '
        f'{get_optional_text(o)}'
    )

    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, depth=depth + 1)


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of class"""
    return '  ' * depth + o.__class__.__name__


def get_optional_fontinfo(o: Any) -> str:
    """Font info of LTChar if available, otherwise empty string"""
    if hasattr(o, 'fontname') and hasattr(o, 'size'):        return f'{o.fontname} {round(o.size)}pt'
    return ''


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()

        # if 'cid' in text:
        #     char_index = int(text[1:-1].split(':')[-1])-1
        #     char = o.
    return ''


path = Path('../data/checkpdf2/278.pdf').expanduser()
pages = extract_pages(path)
show_ltitem_hierarchy(pages)

import re

text = 'BT\n/F1 1 Tf\n22 0 0 22 207.4294 444.0927 Tm\n0 0 0 1 k\n/GS2 gs\n-0.0043 Tc\n0 Tw\n[(\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x04\\x08\\x08\\t\\\\012\\x0b\\x0c)-68.2(\\015\\x04\\x08\\x06\\x0e\\x0b)]'
#
# # Find all matches
# matches = re.findall(pattern, text)
# text = b'BT\n/F1 1 Tf\n22 0 0 22 207.4294 444.0927 Tm\n0 0 0 1 k\n/GS2 gs\n-0.0043 Tc\n0 Tw\n[(\x01\x02\x03\x04\x05\x06\x07\x04\x08\x08\t\\012\x0b\x0c)-68.2(\\015\x04\x08\x06\x0e\x0b)]TJ\n-2.7991 -1.2275 TD\n-0.0042 Tc\n[(\x0f\x10\x0b\x11\x04\x02\x08\t\x12\x13\x0e\x14\x07\t\x07\x14\x15\x0c)-33.5(\x0e\x04\x16\t\x0e\\012\x14\x17\x0c)-33.5(\x18\x0c)-33.5(\x19\x1a\x0c)-33.5(\x1b\x04\x06)]TJ\n/F2 1 Tf\n14 0 0 14 252.4666 362.6941 Tm\n-0.0049 Tc\n[(\x01\x02\x03\x04\x05\x06\x07)-67.9(\x08)]TJ\n11 0 0 11 257.0597 68.1022 Tm\n-0.0038 Tc\n[(\t\\012\x0b\x0c\\015\x0e\x0f\x07)-113.6(\x10\x11\x11\x08)]TJ\n/F1 1 Tf\n30 0 0 30 245.2369 570.9539 Tm\n/GS1 gs\n0.0018 Tc\n(\x1c\x1d\x10\x1e\x1f !)Tj\n-2.1562 -1.2007 TD\n0.0015 Tc\n(\x1c\x01\x10\x10\x1e"\x1f\x01\x1c \x1e\x1d#$\x1f\x01%)Tj\n1.9705 -1.1993 TD\n0.0009 Tc\n(&\x10\x1e \'  )Tj\nET\n'
# s = str(text, 'utf-8')
# # ww = re.findall('/F\d+[^/]*(?:/[^F\d]|$)', s)
# pattern = r'\\F\d+[^\\]*(?:\\[^F\d]|$)'
# matches = re.findall(pattern, s)
# ww = matches
# print(len(ww), ww)

# import re
# text = '''BT\n/F1 1 Tf\n22 0 0 22 207.4294 444.0927 Tm\n0 0 0 1 k\n/GS2 gs\n-0.0043 Tc\n0 Tw\n[(\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x04\\x08\\x08\\t\\\\012\\x0b\\x0c)-68.2(\\015\\x04\\x08\\x06\\x0e\\x0b)]TJ\n-2.7991 -1.2275 TD\n-0.0042 Tc\n[(\\x0f\\x10\\x0b\\x11\\x04\\x02\\x08\\t\\x12\\x13\\x0e\\x14\\x07\\t\\x07\\x14\\x15\\x0c)-33.5(\\x0e\\x04\\x16\\t\\x0e\\\\012\\x14\\x17\\x0c)-33.5(\\x18\\x0c)-33.5(\\x19\\x1a\\x0c)-33.5(\\x1b\\x04\\x06)]TJ\n/F2 1 Tf\n14 0 0 14 252.4666 362.6941 Tm\n-0.0049 Tc\n[(\\x01\\x02\\x03\\x04\\x05\\x06\\x07)-67.9(\\x08)]TJ\n11 0 0 11 257.0597 68.1022 Tm\n-0.0038 Tc\n[(\\t\\\\012\\x0b\\x0c\\\\015\\x0e\\x0f\\x07)-113.6(\\x10\\x11\\x11\\x08)]TJ\n/F1 1 Tf\n30 0 0 30 245.2369 570.9539 Tm\n/GS1 gs\n0.0018 Tc\n(\\x1c\\x1d\\x10\\x1e\\x1f !)Tj\n-2.1562 -1.2007 TD\n0.0015 Tc\n(\\x1c\\x01\\x10\\x10\\x1e"\\x1f\\x01\\x1c \\x1e\\x1d#$\\x1f\\x01%)Tj\n1.9705 -1.1993 TD\n0.0009 Tc\n(&\\x10\\x1e '  )Tj\nET\n'''
# print(repr(text))
#
# pattern = '/F\d+[.\n]*(?=/F\d+)'
# # Find all matches
# matches = re.findall(pattern, text)
#
# for i in matches:
#     print('line', i)
# import re
# pattern = r'(?=F\d)'
#
# result = re.split(pattern, text)
# result = [s.strip() for s in result if s.strip()]
#
# for i in result:
#     print("newline", i)
