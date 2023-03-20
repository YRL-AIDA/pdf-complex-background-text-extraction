import os
import string
from pathlib import Path

from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import glob


def font2png(fonts_folder, save_folder):
    img_height, img_width = 28, 28
    directories = []
    lowerletter = list(string.ascii_lowercase)
    for letter in lowerletter:
        directories.append("./" + save_folder + "/" + letter)
    for dir in directories:
        if os.path.exists(dir):
            for file in glob.glob(dir + "/*.png"):
                os.remove(file)
        else:
            os.makedirs("./" + dir)
    fontsDir = "./" + fonts_folder + "/"
    fontFiles = os.listdir(os.fsencode(fontsDir))
    counter = 0
    for fontFile in fontFiles:
        fontName = os.fsdecode(fontFile)
        for idx, i in enumerate(lowerletter):
            img = Image.new('L', (img_width, img_height))
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype(fontsDir + fontName, 16)
            _, _, w, h = draw.textbbox((0, 0), i, font)

            draw.text(((img_width - w) / 2, (img_height - h) / 2), i, "white", font)
            imgName = i + "_" + str(counter) + ".png"
            img.save("./" + save_folder + "/" + i + "/" + imgName)
        counter += 1


font2png("fontstest", "testimgs")
font2png("fontstrain", "trainimgs")