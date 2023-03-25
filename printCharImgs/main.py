import os
import shutil
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont


def font2png(fonts_folder, save_folder):
    img_height, img_width = 28, 28
    directories = []
    fontsDir = "./" + fonts_folder + "/"
    chars = get_all_chars_set(fontsDir)

    # очистить папку
    if os.path.isdir(save_folder):
        shutil.rmtree(save_folder)
    os.makedirs("./" + save_folder)
    # создать папки
    for char in chars:
        name = symb2str(char)
        os.makedirs("./" + save_folder + "/" + name)

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
        # print(font_chars)
        for char in font_chars:
            img = Image.new('L', (img_width, img_height))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(fontsDir + fontName, 16)
            _, _, w, h = draw.textbbox((0, 0), char, font)
            draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)

            # пустое изображение
            if img.getbbox() is None:
                continue

            # folder_name = symb2str(char)
            # if not os.path.isdir("./" + save_folder + "/" + folder_name):
            #     os.makedirs("./" + save_folder + "/" + folder_name)

            imgName = symb2str(char) + "_" + str(counter) + ".png"
            img.save("./" + save_folder + "/" + symb2str(char) + "/" + imgName)
        counter += 1
    remove_empty_folders(save_folder)


def symb2str(char: str):
    invalid_symbols = {"/": "slash", "\\": "backslash", ":": "colon", "*": "asterisk", "?": "question",
                       "\"": "quotation", "<": "less", ">": "more", "|": "vertical", " ": "space", ".": "dot"}
    return invalid_symbols[char] if char in invalid_symbols else char + "_lower" if char.islower() else char + "_upper"


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

# ŕ есть у некоторых, но нет
# что чًтًоً
# print("ᾒ".encode().decode('utf8').islower())
# print("ᾚ".encode().decode('utf8').islower())
# ὼ Ὼ
font2png("fontsvalidation", "validationimgs")


# os.makedirs("Ὼ")
# os.makedirs("ὼ")