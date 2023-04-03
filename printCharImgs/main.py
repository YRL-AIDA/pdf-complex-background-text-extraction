import os
import shutil
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import configparser
import string

def font2png(fonts_folder, save_folder):
    img_height, img_width = 28, 28
    fontsDir = "./" + fonts_folder + "/"
    # chars = get_all_chars_set(fontsDir)
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    chars = config.get('DEFAULT', 'Symbols')
    chars = set([n.strip() for n in chars])

    if os.path.isdir("./imgs/" + save_folder):
        shutil.rmtree("./imgs/" + save_folder)
    os.makedirs("./imgs/" + save_folder)

    for char in chars:
        name = symb2str(char)
        os.makedirs("./imgs/" + save_folder + "/" + name)

    # for char in chars:
    #     name = symb2str(char)
    #     directories.append("./" + save_folder + "/" + name)
    # for dir in directories:
    #     if os.path.exists(dir):
    #         for file in glob.glob(dir + "/*.png"):
    #             os.remove(file)
    #         os.rmdir(dir)
    # for dir in directories:
    #     print(dir)
    #     os.makedirs(dir)

    counter = 0
    fontFiles = os.listdir(os.fsencode(fontsDir))
    for fontFile in fontFiles:
        fontName = os.fsdecode(fontFile)
        font_chars = get_char_list_from_ttf(fontsDir + fontName)
        for char in chars:
            if char not in font_chars:
                continue
            img = Image.new('L', (img_width, img_height))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(fontsDir + fontName, 16)
            _, _, w, h = draw.textbbox((0, 0), char, font)
            draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)

            # пустое изображение
            if img.getbbox() is None:
                continue

            imgName = symb2str(char) + "_" + str(counter) + ".png"
            img.save("./imgs/" + save_folder + "/" + symb2str(char) + "/" + imgName)
        counter += 1
    # remove_empty_folders(save_folder)


def symb2str(char: str):
    invalid_symbols = {"/": "slash", "\\": "backslash", ":": "colon", "*": "asterisk", "?": "question",
                       "\"": "quotation", "<": "less", ">": "more", "|": "vertical", " ": "space", ".": "dot"}
    # return invalid_symbols[char] if char in invalid_symbols else char + "_lower" if char.islower() else char + "_upper"
    return invalid_symbols[char] if char in invalid_symbols else char + "_lower" if char.islower() else char + "_upper" if char.isupper() else char


def get_all_chars_set(fonts_path):
    chars = set()
    font_files = os.listdir(os.fsencode(fonts_path))
    for fontFile in font_files:
        path = fonts_path + os.fsdecode(fontFile)
        for char in get_char_list_from_ttf(path):
            chars.add(char)
    return chars


def remove_empty_folders(path):
    folders = list(os.walk(path))[1:]
    # print(folders)
    for folder in folders:
        # print(folder)
        if not folder[2]:
            os.rmdir(folder[0])


def get_char_list_from_ttf(font_file):
    f_obj = TTFont(font_file)
    m_dict = f_obj.getBestCmap()
    unicode_list = []
    for key, _ in m_dict.items():
        unicode_list.append(key)

    char_list = [chr(ch_unicode) for ch_unicode in unicode_list if chr(ch_unicode).isprintable()]
    return char_list


font2png("fontstest", "testimgs")
font2png("fontstrain", "trainimgs")
#
# # что чًтًоً
font2png("fontsvalidation", "validationimgs")


# font = TTFont("Regular.otf")
# print('я' in font.getGlyphSet())
# print(list(string.ascii_lowercase + string.ascii_uppercase + str([chr(i) for i in range(ord('а'), ord('я')+1)]) +
#            str([chr(i) for i in range(ord('А'), ord('Я')+1)])))


# l = list(string.ascii_lowercase + string.ascii_uppercase) + [chr(i) for i in range(ord('а'), ord("я")+1)]+ [chr(i) for i in range(ord('А'), ord("Я")+1)] + [chr(i) for i in range(ord('0'), ord("9")+1)]
# # print(list(string.ascii_lowercase + string.ascii_uppercase) + [chr(i) for i in range(ord('а'), ord("я")+1)]
# #       + [chr(i) for i in range(ord('А'), ord("Я")+1)])
#
# print(','.join(l + list(string.punctuation)))
# config = configparser.ConfigParser()
# config.read('config.ini', encoding='utf-8')
# l = config.get('DEFAULT', 'Symbols')
# l = set([n.strip() for n in l])
# print(l)