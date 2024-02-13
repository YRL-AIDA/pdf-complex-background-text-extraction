from cnn_model import Model
from font_recognition import FontRecognizer
from config import DefaultModel
#
fr_rus_eng = FontRecognizer.load_default_model(DefaultModel.Russian_and_English)
# p = "../data/checkpdf/3.pdf"
p = "../data/checkpdf/sample3.pdf"
print(fr_rus_eng.restore_text(p, start_page=0, end_page=1))
# fr_rus_eng.restore_text(p, start_page=0, end_page=1)
# print(fr_rus_eng.restore_text(p, start_page=0, end_page=1))
# p = "../data/checkpdf/4.pdf"
# print(fr_rus_eng.restore_text(p, start_page=0, end_page=1))
# p = "../data/checkpdf/2.pdf"
# print(fr_rus_eng.restore_text(p, start_page=0, end_page=1))

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
