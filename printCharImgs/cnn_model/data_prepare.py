import ast
import glob
import os
import random
import shutil
import subprocess
import warnings
from pathlib import Path
import Augmentor
import PIL.ImageOps
from PIL import ImageFont, Image
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
import cv2
from skimage.util import random_noise
from font_action.draw_glyph import drawglyph_pillow, drawglyph_by_pen
import splitfolders
from os import listdir
from os.path import isfile, join
import config
from src import utils

# images_folder = ""

bottom_align = config.other.get('bottom_align')
dontaug = config.other.get('dont_aug')


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


def add_noise(train_path):
    subfolders = glob.glob(train_path + "/*")
    for subfolder in subfolders:
        if subfolder.split('\\')[-1] in dontaug:
            continue
        elif subfolder.split('\\')[-1] not in dontaug:
            subfolderfiles = glob.glob(subfolder + "/*")
            for imgpath in subfolderfiles:
                if random.random() >= 0.7:
                    img = cv2.imread(imgpath, 0)
                    img = random_noise(img, mode="s&p", clip=True)
                    cv2.imwrite(imgpath, 255 * img)


def generate_imgs_fontforge(save_imgs_folder, font_folder, char_pool):
    fonts_dir = f"{font_folder}/"
    if os.path.isdir(save_imgs_folder):
        shutil.rmtree(save_imgs_folder)
    os.makedirs(save_imgs_folder)
    uni_char_pool = [str(ord(char)) for char in char_pool]
    for char in char_pool:
        os.makedirs(save_imgs_folder + "/" + str(ord(char)))

    counter = 0
    font_files = os.listdir(fonts_dir)
    warnings.filterwarnings("ignore", category=Warning)
    for font_file in font_files:
        font_name = os.fsdecode(font_file)
        font_file_path = fr'"{font_folder}/{font_file}"'
        # for char in char_pool:
        #     try:
        #         DEVNULL = open(os.devnull, 'wb')
        #         result = subprocess.check_output(
        #             f"ffpython  -W ignore ../cnn_model/fontforge_wrapper.py {save_imgs_folder} {font_file_path} {ord(char)} {counter} True", stderr=DEVNULL)
        #     except:
        #         # print("problem", char, font_file)
        #         continue
        #     result = result.decode('utf-8').replace('\r\n', '')
        #     if result == "None":
        #         continue
        #     handle_image(result)
        try:
            print(font_name)
            DEVNULL = open(os.devnull, 'wb')
            # result = subprocess.check_output(f"ffpython ../cnn_model/fontforge_wrapper.py {save_imgs_folder} {font_file_path} {counter} True", stderr=DEVNULL)
            # result = subprocess.check_output(f"ffpython ../cnn_model/fontforge_wrapper.py {save_imgs_folder} {font_file_path} {counter} True {' '.join(uni_char_pool)}", stderr=DEVNULL)
            result = subprocess.check_output(f"ffpython ../cnn_model/fontforge_wrapper.py True {save_imgs_folder} {font_file_path} {counter} {' '.join(uni_char_pool)}", stderr=DEVNULL)
            #result = subprocess.check_output(["ffpython", "../cnn_model/fontforge_wrapper.py", save_imgs_folder, font_file_path, counter, "True"] + uni_char_pool)
            # result = subprocess.check_output(["ffpython", "../cnn_model/fontforge_wrapper.py", save_imgs_folder, font_file_path, str(counter), "True"] + uni_char_pool)
            # result = subprocess.check_output(["ffpython", "../cnn_model/fontforge_wrapper.py", save_imgs_folder, r'"D:/rep/fonts-recognition/printCharImgs/data/fonts/check/Bebas Neue Cyrillic.otf"', str(counter), "True", "q"])
        except:
            continue
        result = result.decode('utf-8')
        result = ast.literal_eval(result)
        for img in result:
            handle_image(img)
        counter += 1


def handle_image(image_path, size: tuple = (28, 28)):
    im = Image.open(image_path)
    # im = PIL.ImageOps.invert(im)
    # im.thumbnail((28, 28), Image.LANCZOS)
    # im.show()
    new_image = Image.new("L", size, color=255)
    x_offset = (new_image.size[0] - im.size[0]) // 2
    y_offset = (new_image.size[1] - im.size[1]) // 2
    new_image.paste(im, (x_offset, y_offset))
    new_image = PIL.ImageOps.invert(new_image)
    # new_image.show()
    new_image.save(image_path)
    # im.save(image_path)

    # im = im.resize(size, Image.LANCZOS)
    # im.save(image_path)


def generate_imgs(save_imgs_folder, font_folder, char_pool):
    img_width, img_height = 28, 28
    # fonts_dir = "./" + font_folder + "/"
    fonts_dir = font_folder + "/"

    if os.path.isdir(save_imgs_folder):
        shutil.rmtree(save_imgs_folder)
    os.makedirs(save_imgs_folder)

    for char in char_pool:
        # print(char, ord(char))
        os.makedirs(save_imgs_folder + "/" + str(ord(char)))
    counter = 0
    font_files = os.listdir(os.fsencode(fonts_dir))
    cnt = 0
    for font_file in font_files:
        font_name = os.fsdecode(font_file)
        print(font_name)
        cnt += 1
        font = ImageFont.truetype(fonts_dir + font_name, 28)
        ttfont = TTFont(fonts_dir + font_name)
        try:
            glyphset = ttfont.getGlyphSet()
        except:
            continue
        size = 0
        msize = 9999
        # for g in glyphset:
        #     bp = BoundsPen(glyphset)
        #     glyph = glyphset[g]
        #     print(glyph)
        #     glyph.draw(bp)
        #     if bp.bounds is None:
        #         continue
        #     if g == 'comma':
        #         comas = abs(bp.bounds[1]) + abs(bp.bounds[3])
        #     size = max(size, abs(bp.bounds[1]) + abs(bp.bounds[3]))
        #     msize = min(msize, abs(bp.bounds[1]) + abs(bp.bounds[3]))
        cmap = ttfont.getBestCmap()
        # важно
        font_chars = get_char_list_from_ttf(fonts_dir + font_name)
        for char in char_pool:
            if char not in font_chars:
                continue
            try:
                img = drawglyph_by_pen(ttfont, cmap[ord(char)], size, 0)
            except:
                continue
            if img is None:
                continue
            # imgName = symb2str(char) + "_" + str(counter) + ".png"
            # img.save(save_folder + "/" + symb2strdir(char) + "/" + imgName)
            imgName = str(ord(char.lower())) + "_" + str(counter) + ".png"
            img.save(save_imgs_folder + "/" + str(ord(char.lower())) + "/" + imgName)
        counter += 1


def generateAugedImgs(imgsfolder, augmentedSave):
    aug_imgs(imgsfolder, augmentedSave)


def prepdata(fonts_path, data_save_path, char_pool):
    images_folder = data_save_path

    # generate_images_path = images_folder + "/images"
    # output_path = images_folder + "/output"
    generate_images_path = f"{images_folder}/images"
    output_path = f"{images_folder}/output"

    generate_imgs(generate_images_path, fonts_path, char_pool)
    if os.path.exists(images_folder + "/output"):
        shutil.rmtree(images_folder + "/output")
    splitfolders.ratio(generate_images_path, output=output_path, ratio=(0.7, 0.2, 0.1), move=False)

    # train_path = output_path + "/train"
    # test_from_train(train_path)


def prepdata_fontforge(fonts_path, data_save_path, char_pool):
    images_folder = data_save_path
    generate_images_path = f"{images_folder}/images"
    output_path = f"{images_folder}/output"
    generate_imgs_fontforge(generate_images_path, fonts_path, char_pool)
    if os.path.exists(images_folder + "/output"):
        shutil.rmtree(images_folder + "/output")
    splitfolders.ratio(generate_images_path, output=output_path, ratio=(0.7, 0.2, 0.1), move=False)


def test_from_train(train_path):
    k = 0
    test_from_train_path = os.path.join(os.path.dirname(train_path), "test_from_train")
    for src_dir, dirs, files in os.walk(train_path):
        dst_dir = src_dir.replace(train_path, test_from_train_path, 1)

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
