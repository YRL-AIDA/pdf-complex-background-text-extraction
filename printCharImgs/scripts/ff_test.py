# import fontforge
# F = fontforge.open("20db.otf")
# # fitzfont = fitz.Font("20db.otf")
# i = 0
# for name in F:
#     i += 1
#     print(i)
#     if i == 6:
#         break
#     filename = name + ".png"
#     F[name].export(f"./folder/{filename}")

# from PIL import Image
# im = Image.open("../scripts/folder/afii10018.png")
# im.thumbnail((28, 28), Image.LANCZOS)
# new_image = Image.new("L", (28, 28))
# x_offset= (new_image.size[0] - im.size[0]) // 2
# y_offset= (new_image.size[1] - im.size[1]) // 2
# new_image.paste(im, (x_offset, y_offset))
# new_image.save("1.png")

# import os
# import subprocess
# from src.utils import get_project_root
# # subprocess.run("ffpython ../cnn_model/fontforge_wrapper.py 1 2 3")
# fonts_path = f"{get_project_root()}/data/fonts/fonts"
# fonts = os.listdir(fonts_path)
# j = 0
# for i in fonts:
#     if j == 10:
#         break
#     j += 1
#     font_path = f"{fonts_path}/{i}"
#     subprocess.run(f"ffpython ../cnn_model/fontforge_wrapper.py 1 {font_path} 3")


# import subprocess
# result = subprocess.check_output(f"ffpython ../cnn_model/fontforge_wrapper.py 1 2 3 4")
# print(result.decode("utf-8"))


from cnn_model import Model
model = Model()
model.prepare_data_fontforge()
