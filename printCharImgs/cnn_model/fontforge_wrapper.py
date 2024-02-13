import sys


# def generate_images(save_path, font_path, uni, index, is_train):
#     import fontforge
#     font = fontforge.open(font_path)
#     glyph_name = fontforge.nameFromUnicode(int(uni))
#     char = chr(int(uni))
#     if is_train == "True" and char.isalpha():
#         if char.isupper():
#             char_low = char.lower()
#             if font[ord(char)] == font[ord(char_low)]:
#                 return "None"
#         ##
#     if glyph_name == -1:
#         return "None"
#     save_path = f"{save_path}/{uni}/{uni}_{index}.png"
#     font[int(uni)].export(save_path, 29)
#     return save_path

def generate_images(save_path, font_path, index, uni_char_pool):
    import fontforge
    font = fontforge.open(font_path)
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
            font[int(uni)].export(char_save_path, 29)
            save_paths.append(char_save_path)
        except:
            continue

    return save_paths

def generate_all_images(save_path, font_path):
    import fontforge
    font = fontforge.open(font_path)
    save_paths = []
    for name in font:
        try:
            filename = str(ord(name)) + ".png"
            char_save_path = f"{save_path}/{filename}"
            # font[name].simplify(flags=("removesingletonpoints"))
            # font[name].simplify()
            # font[name].foreground.isEmpty()
            # font[name].isWorthOutputting()
            w = font[name].width
            # font[name].simplify("removesingletonpoints")
            if w == 0 or not font[name].isWorthOutputting() or font[name].foreground.isEmpty() == 1:
                continue
            font[name].export(char_save_path, 29)
            save_paths.append(char_save_path)
        except:
            continue
    return save_paths



if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "True":
        print(generate_images(args[1], args[2], args[3], args[4:]))
    elif args[0] == "False":
        print(generate_all_images(args[1], args[2]))
