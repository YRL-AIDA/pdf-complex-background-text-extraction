import os

import PIL.ImageOps
from PIL import Image


def correctly_resize(image_path, size: tuple = (28, 28)):
    im = Image.open(image_path)
    new_image = Image.new("L", size, color=255)
    x_offset = (new_image.size[0] - im.size[0]) // 2
    y_offset = (new_image.size[1] - im.size[1]) // 2
    new_image.paste(im, (x_offset, y_offset))
    new_image = PIL.ImageOps.invert(new_image)
    new_image.save(image_path)


def is_empty(image_path) -> bool:
    img = Image.open(image_path)
    extrema = img.convert("L").getextrema()
    if extrema == (255, 255) or extrema == (0, 0):
        return True
    else:
        return False
