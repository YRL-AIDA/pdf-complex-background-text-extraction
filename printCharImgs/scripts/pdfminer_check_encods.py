import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'D:\\soft\\Tesseract\\tesseract.exe'
# img = cv2.imread('D:\\rep\\fonts-recognition\\printCharImgs\\data\\pdfdata\\glyph_images\\KOGJFF+MSTT31c400\\GAB.png')
img = cv2.imread(r'D:\rep\fonts-recognition\printCharImgs\data\datasets\123\images\33\20db_0.png', cv2.IMREAD_GRAYSCALE)
img1 = cv2.imread(r'D:\rep\fonts-recognition\printCharImgs\data\pdfdata\glyph_images\ABCDEE+Calibri-Bold\102.png')
img2 = cv2.imread( 'D:\\rep\\fonts-recognition\\printCharImgs\\data/pdfdata/glyph_images\\ABCDEE+Calibri-Bold\\103.png')
# cv2.imshow('1', img)
# cv2.waitKey(0) B[C7#ИK B0CC7A#0BИ7[Л,#0И /C7ИДИИ 05ЩеcTBеЯЯ0МV цеЯT!V «CV4е5Я0=Л!aB0BaA !е”0!Мa> _ і0 ЛеT *ЖGМНDСР YN$kbЕ@С &РРР
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (3,3), 0)
# thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
# # Morph open to remove noise and invert image
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
# invert = 255 - opening
# cv2.imshow('1', invert)
# cv2.waitKey(0)
# cv2.imshow('1', opening)
# cv2.waitKey(0)

# Perform text extraction
data = pytesseract.image_to_string(img1, lang='rus+eng', config='--psm 10')
print(data.replace('\n', ''))

