import configparser
import os
import re
config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')
convertdictrus = eval(config.get("DEFAULT", "convert_chars_to_rus"))
convertdicteng = eval(config.get("DEFAULT", "convert_chars_to_eng"))
rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'o', 'a', 'c', 'e', 'x', 'k']
eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'о', "а", "с"]

def analize_string(string: str):
    strings = string.split(' ')
    ans = []
    for word in strings:
        analized = analize_word(word)
        if analized is not None:
            ans.append(analize_word(word))
    return " ".join(ans)


def analize_word(string: str):
    l = list(string)
    # if re.search('[а-яА-Я]', string):
    #     # res = "".join([convertdict[item] if item in convertdict else item for item in l])
    #     letters = {x: string.count(x) for x in string}
    #     cyrrilic = 0
    #     latin = 0
    #
    #     return res
    letters = {x: string.count(x) for x in string}
    latin = sum([val for val, key in zip(letters.values(), letters.keys()) if key in eng])
    cyrrilic = sum([val for val, key in zip(letters.values(), letters.keys()) if key in rus])
    converted = string
    if cyrrilic >= latin and latin + cyrrilic > 0:
        converted = "".join([convertdictrus[item] if item in convertdictrus else item for item in l])
    elif latin > cyrrilic:
        converted = "".join([convertdicteng[item] if item in convertdicteng else item for item in l])
    # print(converted, cyrrilic, latin, letters)
    return converted


def correct_text(text: list[str]):
    corrected_text = []
    for page in text:
        if not page.isspace():
            res = analize_string(page)
            corrected_text.append(res)
    return corrected_text
