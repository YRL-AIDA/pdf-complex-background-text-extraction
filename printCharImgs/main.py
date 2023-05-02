import os
import shutil
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import configparser
import Augmentor
import extract_font

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


def font2png(fonts_folder, save_folder, testtrain=0):
    img_height, img_width = 28, 28
    fontsDir = "./" + fonts_folder + "/"
    chars = config.get('DEFAULT', 'Symbols')
    chars = set([n.strip() for n in chars])

    if os.path.isdir("./imgs/" + save_folder):
        shutil.rmtree("./imgs/" + save_folder)
    os.makedirs("./imgs/" + save_folder)

    for char in chars:

        # if char.isupper():
        #     continue

        name = symb2str(char)
        os.makedirs("./imgs/" + save_folder + "/" + name)

    counter = 0
    fontFiles = os.listdir(os.fsencode(fontsDir))
    print(fontFiles)
    if testtrain == 1:
        fontFiles = fontFiles[:len(fontFiles) // 4]

    cnt = 0
    # print(fontFiles)
    for fontFile in fontFiles:
        fontName = os.fsdecode(fontFile)
        print(cnt, fontName)
        cnt += 1

        font_chars = get_char_list_from_ttf(fontsDir + fontName)
        for char in chars:
            if char not in font_chars:
                continue

            # if char.isupper():
            #     continue

            img = Image.new('L', (img_width, img_height))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(fontsDir + fontName, 18)
            _, _, w, h = draw.textbbox((0, 0), char, font)
            draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)

            # пустое изображение
            if img.getbbox() is None:
                continue
            # if char == 'e':
            #     img2 = Image.new('L', (img_width, img_height))
            #     draw2 = ImageDraw.Draw(img2)
            #     _, _, w2, h2 = draw.textbbox((0, 0), 'e', font)
            #     draw2.text(((img_width - w) / 2, (img_height - h) / 2), 'E', "white", font)
            #     if not ImageChops.difference(img,img2).getbbox():
            #         print(fontName)

            imgName = symb2str(char) + "_" + str(counter) + ".png"
            img.save("./imgs/" + save_folder + "/" + symb2str(char) + "/" + imgName)
        counter += 1
    # remove_empty_folders(save_folder)


def font2png_noregdiff(fonts_folder, save_folder, testtrain=False):
    img_height, img_width = 28, 28
    fontsDir = "./" + fonts_folder + "/"
    chars = config.get('DEFAULT', 'Symbols')
    chars = set([n.strip() for n in chars])

    if os.path.isdir(save_folder):
        shutil.rmtree(save_folder)
    os.makedirs(save_folder)

    for char in chars:
        if char.isupper():
            continue
        name = symb2strdir(char)
        os.makedirs(save_folder + "/" + name)

    counter = 0
    fontFiles = os.listdir(os.fsencode(fontsDir))
    print(fontFiles)
    if testtrain:
        fontFiles = fontFiles[:len(fontFiles) // 4]

    cnt = 0
    # print(fontFiles)
    for fontFile in fontFiles:
        fontName = os.fsdecode(fontFile)
        print(cnt, fontName)
        cnt += 1

        font_chars = get_char_list_from_ttf(fontsDir + fontName)
        for char in chars:
            if char not in font_chars:
                continue

            img = Image.new('L', (img_width, img_height))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(fontsDir + fontName, 18)
            _, _, w, h = draw.textbbox((0, 0), char, font)
            draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)

            # пустое изображение
            if img.getbbox() is None:
                continue

            imgName = symb2str(char) + "_" + str(counter) + ".png"
            img.save(save_folder + "/" + symb2strdir(char) + "/" + imgName)
        counter += 1
    # remove_empty_folders(save_folder)


def symb2str(char: str):
    invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
    return invalid_symbols[char] if char in invalid_symbols else char + "_lower" if char.islower() else char + "_upper" if char.isupper() else char


def symb2strdir(char: str):
    invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
    return invalid_symbols[char] if char in invalid_symbols else char


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
    for folder in folders:
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


def generateimgs(save_imgs_folder, fontFolder, isTestFromTrain = False):
    font2png_noregdiff(fontFolder, save_imgs_folder, isTestFromTrain)


def generateAugedImgs(imgsfolder, augmentedSave):
    aug_imgs(imgsfolder, augmentedSave)


def filesize(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])


def aug_imgs(path, savefolder):
    savePath = '/'.join(path.split('/')[:-1])
    if os.path.isdir(savePath + "/" + savefolder):
        shutil.rmtree(savePath + "/" + savefolder)
    for root, dirs, files in os.walk(path):
        p = root.split('/')[-1]
        if len(p) == 0 or p == path.split('/')[-1]:
            continue
        imgspath = '/'.join([root])
        outputpath = ("../" * len(path.split('/'))) + savefolder + "/" + root.split('\\')[-1]
        p = Augmentor.Pipeline(imgspath, outputpath)
        p.zoom(probability=0.3, min_factor=0.8, max_factor=1.5)
        p.random_distortion(probability=0.3, grid_width=4, grid_height=4, magnitude=1)
        p.shear(probability=0.3, max_shear_left=10, max_shear_right=10)
        p.rotate(probability=0.3, max_right_rotation=5, max_left_rotation=5)
        p.sample(filesize(imgspath) * 3)


generateimgs("imgs/trainimgs", "fontstrain")
generateimgs("imgs/validationimgs", "fontsvalidation")
generateimgs("imgs/testimgs", "fontstest")
generateimgs("imgs/testfromtrain", "fontstrain", isTestFromTrain=True)

# generateAugedImgs("imgs/trainimgs", "outputTrain")
# generateAugedImgs("imgs/validationimgs", "outputVal")
# generateAugedImgs("imgs/testimgs", "outputTest")
# generateAugedImgs("imgs/testtrainimgs", "outputTestTrain")

extract_font.extract_pfdfont("pdf/1.pdf")
