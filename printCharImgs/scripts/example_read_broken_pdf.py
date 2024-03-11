from icecream import ic

from cnn_model import Model
from font_recognition import FontRecognizer
from config import DefaultModel
#
fr_rus_eng = FontRecognizer.load_default_model(DefaultModel.Russian_and_English)
# p = "../data/checkpdf/3.pdf"
# p = "../data/checkpdf/sample3.pdf"
# p = "../data/checkpdf/2.pdf"
q = "../data/checkpdf2"
qq = "../data/checkpdf"
qqq = "../data/check_pdf"
# norm = [f'{q}/152.pdf', f'{q}/069.pdf', f'{q}/089.pdf', f'{q}/154.pdf', f'{qq}/mongolo.pdf']
norm = ['154', '278', '767', 'hz', 'hz2', 'hz3']
p = "../data/checkpdf2/278.pdf"
ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/w2.pdf', start_page=0, end_page=1))
# ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/5.pdf', start_page=0, end_page=1))
# ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/6.pdf', start_page=0, end_page=1))
# ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/8.pdf', start_page=0, end_page=1))
# ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/9.pdf', start_page=0, end_page=1))
# ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/10.pdf', start_page=0, end_page=1))
# ic(fr_rus_eng.restore_text_fontforge(f'{qqq}/11.pdf', start_page=0, end_page=1))

# print(fr_rus_eng.restore_text_fontforge(f'{q}/q.pdf', start_page=0, end_page=1))

#
# import text_action.analize
# print('Hиman'.lower())
# print(text_action.analize.find_closest_word('austrazian'))
import re

# cc = re.findall(r'(?:\w\S*\w)|(?:\S)|(?: )', 'big f,c|ing| cock')
# cc = re.findall(r'\b\w+\b|[,. ]', 'big, f,c|ing| cock')
# cc = re.findall(r'\b\w+\b|[\w,]+|[.,\s]', 'big, f,c|ing| house')
# cc = re.findall(r'(?:\S+(?=[,\.]\s)|(?:\S+(?=\s|$))|(?:\s))', 'q.er., asdf zxcv. asdas')
# print(cc)
# print(''.join(cc))

# print(re.findall(r'(?:\w\S*\w)|(?:\S)|(?: )', 'big f,c|ing, cock'))
# (cid:01) ' '
# \GDE \GDA \GDB
# \x01 \x02 \x03
# \Differer
#Contact us here secunet.com/safesurfer □□□□□□□□□□□ '
#'□□□□□□□□□□□□□□□□□□ □□□□□□□□□□□□□□□□□□ □□□□□□□□□□□ secunet is а security '
#'partner of the German Federal Government and а member of all relevant '
#'industry associations. ')
#
