import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'D:\\soft\\Tesseract\\tesseract.exe'
# img = cv2.imread('D:\\rep\\fonts-recognition\\printCharImgs\\data\\pdfdata\\glyph_images\\KOGJFF+MSTT31c400\\GAB.png')
img = cv2.imread(r'C:\Users\user\Downloads\okbRqBL-GIo.jpg')
# img1 = cv2.imread(r'D:\rep\fonts-recognition\printCharImgs\data\pdfdata\glyph_images\ABCDEE+Calibri-Bold\102.png')
# img2 = cv2.imread( 'D:\\rep\\fonts-recognition\\printCharImgs\\data/pdfdata/glyph_images\\ABCDEE+Calibri-Bold\\103.png')

# Perform text extraction
data = pytesseract.image_to_string(img, lang='rus')
print(data.replace('\n', ''))

