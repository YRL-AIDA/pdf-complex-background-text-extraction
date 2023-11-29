from model.data_prepare import prepdata
from model.data_prepare import listFonts

from PDFData import gettext
# prepdata()
text = gettext("PDF/1.pdf")
for i in text:
    print(i)
# print(listFonts("./fonts/fonts"))
import PDFData
