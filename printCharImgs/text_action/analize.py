import configparser
import os
import re
import warnings

from typing import List

from Levenshtein import distance
# import editdistance as editdistance
import numpy as np

config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.ini')
config.read(config_p, encoding='utf-8')
convertdictrus = eval(config.get("DEFAULT", "convert_chars_to_rus"))
# convertdicteng = eval(config.get("DEFAULT", "convert_chars_to_eng"))
convertdicteng = dict((v, k) for k, v in convertdictrus.items())

rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
       'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'o', 'a', 'c', 'e', 'x', 'k']
eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
       'w', 'x', 'y', 'z', 'о', "а", "с"]
onlyRus = ['я', 'й', 'ц', 'б', 'ж', 'з', 'д', 'л', 'ф', 'ш', 'щ', "ч", "ъ", "ь", "э", "ю", 'т', 'г']
onlyEng = ['q', 'w', 'f', 'i', 'j', 'l', 'z', 's', 'v', 'g']
warnings.warn('G/g это onlyEng????????????????? т/Т ???')

import difflib

from nltk.corpus import words

from main import ROOT_DIR

english_words = set(words.words())
with open(f'{ROOT_DIR}/data/russian.txt') as f:
    russian_words = set(f.read().splitlines())

rus_and_eng_names = list(english_words | russian_words)

max_length = max(len(s) for s in rus_and_eng_names)
result = [[] for _ in range(max_length + 1)]

for string in rus_and_eng_names:
    length = len(string)
    result[length].append(string)

rus_and_eng_names = result


def analise_string(string: str):
    strings = string.split(' ')
    ans = []
    for word in strings:
        analized = analise_word(word)
        if analized is not None:
            ans.append(analise_word(word))
    return " ".join(ans)


def analise_word(string: str):
    l = list(string)
    letters = {x: string.count(x) for x in string}
    latin = sum([val for val, key in zip(letters.values(), letters.keys()) if key in eng])
    cyrrilic = sum([val for val, key in zip(letters.values(), letters.keys()) if key in rus])

    converted = string
    if (cyrrilic >= latin and latin + cyrrilic > 0) or any(char in string.lower() for char in onlyRus):
        # converted = "".join([(convertdictrus[item] if item.islower() else convertdictrus[item.lower()].upper())
        #                      if item.lower() in convertdictrus else item for item in l])
        converted = substitute_chars_by_dict(convertdictrus, l)
    elif latin > cyrrilic or any(char in string.lower() for char in onlyEng):
        # converted = "".join([(convertdicteng[item] if item.islower() else convertdicteng[item.lower()].upper())
        #                      if item.lower() in convertdicteng else item for item in l])
        converted = substitute_chars_by_dict(convertdicteng, l)
    return converted


def substitute_chars_by_dict(dict, word):
    return "".join([(dict[item] if item.islower() else dict[item.lower()].upper())
                    if item.lower() in dict else item for item in word])


def correct_text(text: List[str]):
    corrected_text = []
    for page in text:
        if not page.isspace():
            res = analise_string(page)
            res = correct_case(res)
            corrected_text.append(res)
    return corrected_text


def correct_case(string: str):
    new_string = ''
    for i in range(len(string)):
        if i == 0:
            new_string += string[i]
        elif string[i - 1].isalpha() and string[i - 1].islower() and i + 1 < len(string) and string[i + 1].isalpha() and \
                string[i + 1].islower():
            new_string += string[i].lower()
        elif string[i - 1].isalpha() and string[i - 1].isupper() and i + 1 < len(string) and string[i + 1].isalpha() and \
                string[i + 1].isupper():
            new_string += string[i].upper()
        else:
            new_string += string[i]
    return new_string


def t9_text(text):
    words = re.findall(r'(?:\S+(?=[,\.]\s)|(?:\S+(?=\s|$))|(?:\s))', text)
    new_words = []
    for i in words:
        if len(i) == 1:
            new_words.append(i)
            continue
        corrected_word = find_closest_word(i)
        new_words.append(corrected_word)

    new_text = ''.join(new_words)
    return new_text


def find_closest_word(word):
    w1 = word.lower()
    # c1 = difflib.get_close_matches(w1, rus_and_eng_names[len(word)], n=5, cutoff=0.7)
    # if not c1:
    #     # r = substitute_chars_by_dict(convertdictrus, w1)
    #     # e = substitute_chars_by_dict(convertdicteng, w1)
    #     # c1 = (t := difflib.get_close_matches(r, rus_and_eng_names[len(word)], n=5,cutoff=0.9)) if t else c1 = difflib.get_close_matches(e, rus_and_eng_names[len(word)], n=5, cutoff=0.7)
    #     # c1 = t if (t := difflib.get_close_matches(r, rus_and_eng_names[len(word)], n=5, cutoff=0.9)) else difflib.get_close_matches(e, rus_and_eng_names[len(word)], n=5, cutoff=0.9)
    #     # if not c1:
    #     #     return word
    #     return word
    # ans = c1[0]
    #T t m M
    #Т т м М
    if word == 'uhcmumym':
            qqqq = 1

    distances = np.array([distance(w1, i.lower(), weights=(1000, 1000, 1)) for i in rus_and_eng_names[len(w1)]])
    if distances.size == 0:
        return word
    if 1 - np.min(distances) / len(w1) < 0.8:
        r = substitute_chars_by_dict(convertdictrus, w1)
        e = substitute_chars_by_dict(convertdicteng, w1)
        rd = np.array([distance(r, i.lower(), weights=(1000, 1000, 1)) for i in rus_and_eng_names[len(w1)]])
        ed = np.array([distance(e, i.lower(), weights=(1000, 1000, 1)) for i in rus_and_eng_names[len(w1)]])
        d = rd if np.min(rd) < np.min(ed) else ed
        if d.size == 0 or 1 - (np.min(d) / len(w1)) < 0.8:
            return word
        distances = d
    min_index = int(np.argmin(distances))
    ans2 = rus_and_eng_names[len(word)][min_index]
    if word.isupper():
        ans2 = ans2.upper()
    elif word[0].isupper():
        ans2 = ans2.capitalize()
    return ans2
    # if closest_match:
    #     return closest_match[0]
    # else:
    #     return word


# аustrаiаsiаn
# austraiasian
# difflib.get_close_matches('austraiasian', rus_and_eng_names[len(word)], n=5, cutoff=0.8)
def correct_text2(text):
    text = analise_string(text)
    text = correct_case(text)
    return text


def correct_text_str(text):
    return analise_string(text)
