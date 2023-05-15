from PIL import Image, ImageOps, ImageDraw
import fontTools
from fontTools import ttLib
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import os
import shutil
import fitz
from fontTools.ttLib import TTFont


def __draw_glyphs(save_path="pdfdata/glyphimages", fonts_path="pdfdata/extracted_font"):
    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    font_files = os.listdir(os.fsencode(fonts_path))
    counter = 0
    for font_file in font_files:
        fontname = os.fsdecode(font_file)
        font = TTFont(fonts_path + "/" + fontname)
        # font = ttLib.SFNTReader(fonts_path + "/" + fontname)
        # font = fontTools
        # font = fontTools.cffLib.CFFFontSet.convertCFFToCFF2(fonts_path + "/" + fontname)
        os.makedirs(save_path + "/" + fontname)
        glyphset = font.getGlyphSet()
        size = 0
        for g in glyphset:
            glyph = glyphset[g]
            size = max(size, glyph.width)
        for g in glyphset:
            pen = FreeTypePen(glyphset)
            # pen = T2CharStringPen(glyphSet=glyphset)
            bp = BoundsPen(glyphset)
            glyph = glyphset[g]
            glyph.draw(pen)
            glyph.draw(bp)
            if bp.bounds is None:
                continue
            # img = pen.image(width=glyph.width, height=max(glyph.width, 1000), contain=True)
            # img = pen.image(width=glyph.width, height=glyph.width, contain=True)
            # img = pen.image(width=glyph.width, height=10000, contain=True)
            # img = pen.image(width=2000, height=2000, contain=True)
            # img = pen.image(width=glyph.width, height=glyph.width)
            img = pen.image(width=glyph.width, height=1000, contain=True)

            # pen = FreeTypePen(glyphset)
            # glyph.draw(pen)
            print(counter, img.size)
            # img = pen.image(width=max(img.size), height=max(img.size), contain=True)

            background = Image.new('LA', img.size, (255, 255))
            alpha_composite = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))
            alpha_composite = alpha_composite.convert("L")
            alpha_composite = alpha_composite.resize((28, 28))
            alpha_composite = ImageOps.invert(alpha_composite)
            # alpha_composite = alpha_composite.resize((28, 28))

            # alpha_composite.show()
            alpha_composite.save(save_path + "/" + fontname + "/" + str(counter) + ".png")
            # img.save(save_path + "/" + fontname + "/" + str(counter) + ".png")
            # print(save_path + "/" + fontname + "/" + str(counter) + ".png")
            counter += 1


def __extract_pfdfonts(pdf_path, save_path="pdfdata/extracted_font"):
    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    doc = fitz.open(pdf_path)
    xref_visited = []
    dir = save_path + "/"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    for page_num in range(doc.page_count):
        page = doc.get_page_fonts(page_num)
        print(page)
        for fontinfo in page:
            xref = fontinfo[0]
            if xref in xref_visited:
                continue
            xref_visited.append(xref)
            # name, ext, _, content = doc.extract_font(xref, named=True)
            font = doc.extract_font(xref, named=True)
            print(font)
            # name = name.split("+", 1)[1] if "+" in name else name
            if font['ext'] != "n/a":
                ofile = open(dir + font['name'] + "." + font['ext'], "wb")
                print(dir + font['name'] + "." + font['ext'])
                ofile.write(font['content'])
                ofile.close()
    doc.close()


def restore_encoding(pdf_path):
    __extract_pfdfonts(pdf_path)
    __draw_glyphs()
