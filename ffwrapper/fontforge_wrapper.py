import sys
import warnings

import fontforge
from pathlib import Path

image_size = 80


def generate_images(save_path: Path, font_path: Path, index: int, uni_char_pool: list) -> list:

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
        char_save_path = save_path.joinpath(str(uni), f"{font.fontname}_{index}.png")

        try:
            font[int(uni)].export(char_save_path, image_size)
            save_paths.append(char_save_path)
        except:
            continue

    return save_paths


def generate_all_images(save_path: Path, font_path: Path) -> list:
    font = fontforge.open(font_path)
    save_paths = []
    for name in font:
        try:
            if 'superior' in name:
                continue
            if not font[name].isWorthOutputting() and name != 'space':
                continue
            try:
                filename = str(ord(name)) + ".png"
            except:
                unicode_by_name = str(fontforge.unicodeFromName(name))
                if unicode_by_name == '-1' and name == '.notdef':
                    continue

                if unicode_by_name == '-1':
                    filename = name + ".png"
                else:
                    filename = unicode_by_name + '.png'
            char_save_path = f"{save_path}/{filename}"
            if name == ".notdef" or filename == '-1.png':
                continue
            font[name].export(char_save_path, image_size)
            save_paths.append(char_save_path)
        except:
            continue
    return save_paths


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "True":
        print(generate_images(Path(args[1]), Path(args[2]), int(args[3]), args[4:]))
    elif args[0] == "False":
        print(generate_all_images(Path(args[1]), Path(args[2])))
