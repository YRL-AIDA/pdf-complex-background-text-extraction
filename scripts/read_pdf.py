from pdf_worker.pdf_reader import PDFReader
from pathlib import Path

pdf_path = Path("D:\\aus.pdf")
reader = PDFReader.load_default_model("ruseng")
text = reader.restore_text(pdf_path)
print(text)
