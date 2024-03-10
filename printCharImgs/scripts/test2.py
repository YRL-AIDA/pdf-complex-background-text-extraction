from pdfminer.high_level import extract_text
import PyPDF2

with open('../data/checkpdf2/hz3.pdf','rb') as f:
        # pdf_reader = PyPDF2.PdfReader(f)
        # page = pdf_reader.pages[0]
        # text = page.extract_text()

        # get the text content of the page
        # text = page.extracttext()
        text = extract_text(f, page_numbers=[1])
print(' '.join(text.split()))
