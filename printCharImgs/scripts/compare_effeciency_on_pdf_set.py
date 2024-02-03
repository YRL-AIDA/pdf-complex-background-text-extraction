import os

pdfs_path = "../data/pdf"
pdfs_dir = os.fsencode(pdfs_path)
print(pdfs_dir)
for pdf in os.listdir(pdfs_dir):
    print(pdf.decode())
