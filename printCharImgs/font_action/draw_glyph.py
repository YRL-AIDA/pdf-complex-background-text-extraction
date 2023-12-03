import configparser
import os
from PIL.ImageFont import ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
from PIL import Image, ImageOps, ImageDraw
from fontTools.pens.boundsPen import BoundsPen

config = configparser.ConfigParser()
config_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_p, encoding='utf-8')

import config
bottom_align = config.other.get('bottom_align')


def drawglyph_by_pen(ttfont: TTFont, glyph_name, size, minsize):
    # print(t, glyph_name)
    glyphset = ttfont.getGlyphSet()
    pen = FreeTypePen(glyphset)
    glyph = glyphset[glyph_name]
    # a = glyphset['A']
    bp = BoundsPen(glyphset)
    # bpa = BoundsPen(glyphset)
    glyph.draw(bp)
    # a.draw(bpa)

    if bp.bounds is None:
        return None
    glyph.draw(pen)
    img = pen.image(width=glyph.width, contain=True)
    background = Image.new('LA', img.size, (255, 255))
    img = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
    img = img.convert("L")
    # img.thumbnail((22, 22))
    img.thumbnail((18, 18))
    img = ImageOps.invert(img)
    new_im = Image.new("L", (28, 28))
    box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
    new_im.paste(img, box)
    img = new_im

    return img


def drawglyph_pillow(font: ImageFont, char: str, size: tuple):
    img1 = Image.new("L", (size[0], size[1]))
    draw1 = ImageDraw.Draw(img1)
    _, _, w1, h1 = draw1.textbbox((0, 0), "□", font)
    draw1.text(((size[0] - w1) / 2, (size[0] - h1) / 2), "□", "white", font)
    img = Image.Image()._new(font.getmask(char))
    if char == '-':
        img.resize((28, 28))
    else:
        img.thumbnail((28, 28))
    # ???
    if char in bottom_align:
        box = ((28 - img.size[0]) // 2, 28 - img.size[1])
    else:
        box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
    # ???
    new_im = Image.new("L", (28, 28))
    new_im.paste(img, box)
    img = new_im
    if img1 == img or img.getbbox() is None:
        img = None
    # пустое изображение
    return img


def drawglyph_bypen_and_code(_cmap, _glyphset, glyph_code):
    cmap = _cmap
    glyphset = _glyphset
    glyph = glyphset[cmap[glyph_code]]
    pen = FreeTypePen(glyphset)
    bp = BoundsPen(glyphset)
    glyph.draw(bp)

    if bp.bounds is None:
        return None
    glyph.draw(pen)
    if bp.bounds[1] > 0:
        img = pen.image(width=glyph.width, height=bp.bounds[1] // 2 + bp.bounds[3] // 2, contain=True)
    else:
        img = pen.image(width=glyph.width, height=1300, contain=True)
    background = Image.new('LA', img.size, (255, 255))
    img = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
    img = img.convert("L")
    img.thumbnail((22, 22))
    img = ImageOps.invert(img)
    new_im = Image.new("L", (28, 28))
    box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
    new_im.paste(img, box)
    img = new_im
    return img
