import configparser
import glob
import os
import random
import shutil
from pathlib import Path

import Augmentor
from PIL import ImageFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
import cv2
from skimage.util import random_noise
import ast
from DrawGlyph import drawglyph_pillow, drawglyph_bypen_and_code, drawglyph_by_pen
import splitfolders
from os import listdir
from os.path import isfile, join

config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')
bottom_align = config.get("DEFAULT", "bottom_align")
bottom_align = set([n.strip() for n in bottom_align])
punctuation = eval(config.get("DEFAULT", "punctuation"))
invalid_symbols = eval(config.get("DEFAULT", "invalidSymbols"))
images_folder = config.get("FOLDERS", "images_folder")
fonts_folder = config.get("FOLDERS", "fonts_folder")

dontaug = ast.literal_eval(config.get("DEFAULT", "dont_aug"))


def font2png(fonts_folder, save_folder, testtrain=0):
    img_width, img_height = 28, 28
    fontsDir = "./" + fonts_folder + "/"

    if os.path.isdir(save_folder):
        shutil.rmtree(save_folder)
    os.makedirs(save_folder)

    for char in chars:
        name = symb2str(char)
        os.makedirs(save_folder + "/" + name)

    counter = 0
    fontFiles = os.listdir(os.fsencode(fontsDir))
    if testtrain == 1:
        fontFiles = fontFiles[:len(fontFiles) // 4]

    cnt = 0
    for fontFile in fontFiles:
        fontName = os.fsdecode(fontFile)
        print(cnt, fontName)
        cnt += 1
        font = ImageFont.truetype(fontsDir + fontName, 28)
        font_chars = get_char_list_from_ttf(fontsDir + fontName)
        # try:
        #     ttfont = TTFont(fontsDir + fontName)
        #     cmap = ttfont.getBestCmap()
        #     glyphset = ttfont.getGlyphSet()
        #     for char in chars:
        #         if char not in font_chars:
        #             continue
        #
        #         # img = Image.new('L', (img_width, img_height))
        #         # draw = ImageDraw.Draw(img)
        #         # font = ImageFont.truetype(fontsDir + fontName, 18)
        #         # _, _, w, h = draw.textbbox((0, 0), char, font)
        #         # draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)
        #         #
        #         # # пустое изображение
        #         # if img.getbbox() is None:
        #         #     continue
        #         if char.islower():
        #             img1 = Image.Image()._new(font.getmask(char))
        #             img2 = Image.Image()._new(font.getmask(char.upper()))
        #             if img1 == img2:
        #                 continue
        #         img = drawglyph_bypen_and_code(cmap, glyphset, ord(char))
        #         imgName = symb2str(char) + "_" + str(counter) + ".png"
        #         img.save(save_folder + "/" + symb2str(char) + "/" + imgName)
        #         # img = drawglyph_pillow(font, char, (img_width, img_height))
        #         # if img is None:
        #         #     continue
        #         # imgName = symb2str(char) + "_" + str(counter) + ".png"
        #         # img.save(save_folder + "/" + symb2str(char) + "/" + imgName)
        #     counter += 1
        # except Exception:
        #     pass
        for char in chars:
            if char not in font_chars:
                continue
            # img = Image.new('L', (img_width, img_height))
            # draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(fontsDir + fontName, 18)
            # _, _, w, h = draw.textbbox((0, 0), char, font)
            # draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)
            #
            # # пустое изображение
            # if img.getbbox() is None:
            #     continue
            img = drawglyph_pillow(font, char, (img_width, img_height))
            # img = drawglyph_by_pen(ttfont, char, )
            if img is None:
                continue
            imgName = symb2str(char) + "_" + str(counter) + ".png"
            img.save(save_folder + "/" + symb2str(char) + "/" + imgName)
        counter += 1
    # remove_empty_folders(save_folder)


def font2png_noregdiff(fonts_folder, save_folder, testtrain=False):
    img_width, img_height = 28, 28
    fontsDir = "./" + fonts_folder + "/"

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
    if testtrain:
        fontFiles = fontFiles[:len(fontFiles) // 4]

    cnt = 0
    # print(fontFiles)
    for fontFile in fontFiles:
        fontName = os.fsdecode(fontFile)
        cnt += 1
        # важно
        font = ImageFont.truetype(fontsDir + fontName, 28)
        ttfont = TTFont(fontsDir + fontName)
        try:
            glyphset = ttfont.getGlyphSet()
        except:
            continue
        size = 0
        msize = 9999
        comas = 0
        for g in glyphset:
            bp = BoundsPen(glyphset)
            glyph = glyphset[g]
            glyph.draw(bp)
            if bp.bounds is None:
                continue
            if g == 'comma':
                comas = abs(bp.bounds[1]) + abs(bp.bounds[3])
            size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
            msize = min(msize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
        cmap = ttfont.getBestCmap()
        # важно
        font_chars = get_char_list_from_ttf(fontsDir + fontName)
        for char in chars:
            if char not in font_chars:
                continue

            # img = Image.new('L', (img_width, img_height))
            # draw = ImageDraw.Draw(img)
            # # font = ImageFont.truetype(fontsDir + fontName, 18)
            # _, _, w, h = draw.textbbox((0, 0), char, font)
            # draw.text(((img_width - w) / 2, (img_height - h) / 2), char, "white", font)
            # if char in align:
            #     # al = align.get(char)
            #     print(align.get(char))
            #     # img = Image.Image()._new(font.getmask(char, anchor=align.get(char)))
            #     img = Image.Image()._new(font.getmask(char))
            # else:
            #     img = Image.Image()._new(font.getmask(char))
            # ttfont = TTFont(fontsDir + fontName)
            # if char in punctuation:
            #     try:
            #         img = DrawGlyph.drawglyph_by_pen(ttfont, punctuation[char])
            #         if img != img2:
            #             # img.show()
            #             img.save(save_folder + "/" + symb2strdir(char) + "/" + imgName)
            #             continue
            #     except Exception:
            #         # print(str(cnt) + " " + fontName + " no glyphset")

            # img = drawglyph_pillow(font, char, (img_width, img_height))
            try:
                img = drawglyph_by_pen(ttfont, cmap[ord(char)], size, 0)
            except:
                continue
            if img is None:
                continue
            imgName = symb2str(char) + "_" + str(counter) + ".png"
            img.save(save_folder + "/" + symb2strdir(char) + "/" + imgName)
            # img.save(save_folder + "/" + symb2str(char) + "/" + imgName)
        counter += 1
    # remove_empty_folders(save_folder)


def symb2str(char: str):
    return invalid_symbols[char] if char in invalid_symbols else char + "_lower" \
        if char.islower() else char + "_upper" if char.isupper() else char


def symb2strdir(char: str):
    t = invalid_symbols[char] if char in invalid_symbols else char
    t = t.split("_lower")[0]
    t = t.split("_upper")[0]
    return t


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
        if root.split('\\')[-1] in dontaug:
            copyto = imgspath.split('/')[0] + "/" + savefolder + "/" + root.split('\\')[-1]
            os.makedirs(copyto)
            shutil.copytree(imgspath, copyto, dirs_exist_ok=True)
            continue
        elif root.split('\\')[-1] not in dontaug:
            p = Augmentor.Pipeline(imgspath, outputpath)
            p.zoom(probability=0.1, min_factor=0.7, max_factor=1.3)
            # p.random_distortion(probability=0.3, grid_width=2, grid_height=2, magnitude=1)
            # p.shear(probability=0.3, max_shear_left=10, max_shear_right=10)
            # p.rotate(probability=0.3, max_right_rotation=5, max_left_rotation=5)
            p.sample(filesize(imgspath) * 3)


def add_noise(path=images_folder + "/outputTrain"):
    subfolders = glob.glob(path + "/*")
    for subfolder in subfolders:
        if subfolder.split('\\')[-1] in dontaug:
            continue
        elif subfolder.split('\\')[-1] not in dontaug:
            subfolderfiles = glob.glob(subfolder + "/*")
            for imgpath in subfolderfiles:
                if random.random() >= 0.7:
                    img = cv2.imread(imgpath, 0)
                    img = random_noise(img, mode="s&p", clip=True)
                    cv2.imwrite(imgpath, 255*img)


def generateimgs(save_imgs_folder, fontFolder, isTestFromTrain=False):
    font2png_noregdiff(fontFolder, save_imgs_folder, isTestFromTrain)
    # font2png(fontFolder, save_imgs_folder, isTestFromTrain)


def generateAugedImgs(imgsfolder, augmentedSave):
    aug_imgs(imgsfolder, augmentedSave)


def prepdata(charPool = 'RusEng'):
    assert charPool == 'RusEng' or charPool == 'Eng' or charPool == 'Rus', 'no such charPool'
    if charPool == 'RusEng':
        ininame = 'Symbols'
    elif charPool == 'Eng':
        ininame = 'EngAndPunc'
    else:
        ininame = 'RusAndPunc'
    global chars
    chars = config.get('DEFAULT', ininame)
    chars = set([n.strip() for n in chars])

    # generateimgs("imgs/trainimgs", "fonts/fontstrain")
    # generateimgs("imgs/validationimgs", "fonts/fontsvalidation")
    # generateimgs("imgs/train_and_val", "fonts/fonts")
    # generateimgs("imgs/testimgs", "fonts/fontstest")
    # generateimgs("imgs/testfromtrain", "fonts/fontstrain", isTestFromTrain=True)
    generateimgs(images_folder + "/images", fonts_folder)
    splitfolders.ratio(images_folder + "/images", output=images_folder + "/output", ratio=(0.7, 0.2, 0.1), move=False)
    test_from_train()
    # generateAugedImgs("imgs/trainimgs", "outputTrain")
    # add_noise()


def test_from_train():
    k = 0
    dir = images_folder + "/output/train"
    for src_dir, dirs, files in os.walk(dir):
        # dst_dir = src_dir.replace(dir, "img\\output\\test_from_train", 1)
        dst_dir = src_dir.replace(dir, images_folder + "/output/test_from_train", 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        if 'test_from_train' in dst_dir.split('\\')[-1]:
            continue

        list_of_imgs = list(Path(src_dir).rglob('*' + '.png'))

        if k == 0:
            k = int(len(list_of_imgs) * 0.2)

        pngs = random.sample(files, k=k)
        for file_ in pngs:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def listFonts(fontfolder):
    fileswithnum = []
    ind = 1
    print(enumerate(listdir(fontfolder)), listdir(fontfolder))
    for i in listdir(fontfolder):
        if isfile(join(fontfolder, i)):
            fileswithnum.append((ind, i))
            ind += 1
    return fileswithnum
