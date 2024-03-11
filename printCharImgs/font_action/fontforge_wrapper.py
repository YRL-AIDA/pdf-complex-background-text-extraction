import sys
import warnings

import fontforge
from src.utils import append_junk

image_size = 80


def generate_images(save_path, font_path, index, uni_char_pool):

    font = fontforge.open(font_path, 1)
    save_paths = []
    for uni in uni_char_pool:
        uni = int(uni)
        glyph_name = fontforge.nameFromUnicode(uni)
        char = chr(uni)
        try:
            if char.isalpha() and char.isupper():
                char_low = char.lower()
                if font[ord(char)] == font[ord(char_low)]:
                    continue
        except:
            continue
            ##
        if glyph_name == -1:
            continue
        char_save_path = f"{save_path}/{uni}/{font.fontname}_{index}.png"

        try:
            font[int(uni)].export(char_save_path, image_size)
            save_paths.append(char_save_path)
        except:
            continue

    return save_paths



def generate_all_images(save_path, font_path):
    font = fontforge.open(font_path)
    save_paths = []
    # names = []
    counter = 0
    empty_imgs = {}
    for name in font:
        # names.append(name)
        try:
            counter += 1
            if name == 'space':
                empty_imgs[' '] = ' '
                continue
            if not font[name].isWorthOutputting():
                continue
            # if name.startswith('glyph'):
            #     # name = chr(int(name.removeprefix('glyph')))
            try:
                # filename = str(ord(name)) + ".png"
                filename = str(ord(name))
                # filename = save_name + ".png"
            except:
                # try:
                #     filename = str(fontforge.unicodeFromName(name)) + ".png"
                # except:
                #     filename = name + ".png"
                unicode_by_name = str(fontforge.unicodeFromName(name))
                if unicode_by_name == '-1' and name == '.notdef':
                    continue

                if unicode_by_name == '-1':
                    # filename = name + ".png"
                    filename = name
                else:
                    filename = unicode_by_name

            filename = append_junk(filename, counter)
            filename = f'{filename}.png'
            char_save_path = f"{save_path}/{filename}"
            if name == ".notdef" or filename == '-1.png':
                continue
            # font[name].export(char_save_path, 29)
            if (font[name].width == 0 or font[name].foreground.isEmpty() == 1) and len(font[name].references) == 0:
                # empty_imgs.append(name)
                empty_imgs[name] = ' '
                continue

            font[name].export(char_save_path, image_size)
            save_paths.append(char_save_path)
        except:
            continue
    return save_paths, empty_imgs


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "True":
        print(generate_images(args[1], args[2], args[3], args[4:]))
    elif args[0] == "False":
        print(generate_all_images(args[1], args[2]))
