from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
from PIL import Image, ImageFont, ImageDraw, ImageOps
from fontTools.pens.boundsPen import BoundsPen


def drawglyph_by_pen(ttfont: TTFont, glyph_name, size, counter):
    # print(t, glyph_name)
    glyphset = ttfont.getGlyphSet()
    pen = FreeTypePen(glyphset)
    glyph = glyphset[glyph_name]
    bp = BoundsPen(glyphset)
    glyph.draw(bp)
    if bp.bounds is None:
        return None
    # img = pen.image(width=glyph.width, height=abs(bp.bounds[1] + bp.bounds[3]), contain=True)
    # pen = FreeTypePen(None)
    # glyph = ttfont.getGlyphSet()[ttfont]
    glyph.draw(pen)
    # print(glyph_name)
    if bp.bounds[1] > 0:
        # print(1, bp.bounds)
        # img = pen.image(width=glyph.width, height=(bp.bounds[1] + bp.bounds[3]) / 2, contain=True)
        img = pen.image(width=glyph.width, height=bp.bounds[1]//2 + bp.bounds[3]//2, contain=True)
        # img = pen.image(width=glyph.width, contain=True)
    else:
        # print(2)
        # img = pen.image(width=glyph.width, height=1300, contain=True)
        # img = pen.image(width=glyph.width, height=size[1]*0.9, contain=True)
        print(counter)
        # img = pen.image(width=glyph.width, contain=True)
        img = pen.image(width=glyph.width, height=size//3, contain=True)
        # img = pen.image(width=size[0], height=size[1], contain=True)
    # print(img.size)
    background = Image.new('LA', img.size, (255, 255))
    img = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
    img = img.convert("L")
    img.thumbnail((22, 22))
    # alpha_composite.show()
    img = ImageOps.invert(img)
    new_im = Image.new("L", (28, 28))
    box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
    new_im.paste(img, box)
    img = new_im

    # background = Image.new('LA', img.size, (255, 255))
    # img = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
    # # img.show()
    # img = img.convert("L")
    # img.thumbnail((26, 26))
    # # img.show()
    # img = ImageOps.invert(img)
    # new_im = Image.new("L", (28, 28), color=0)
    #
    # box = tuple((n - o) // 2 for n, o in zip((28, 28), img.size))
    # new_im.paste(img, box)
    # img = new_im

    return img
