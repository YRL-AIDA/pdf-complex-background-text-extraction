import os
import shutil
import fitz


def extract_pfdfont(pdf_path, tosave="extracted_font"):
    doc = fitz.open(pdf_path)
    xref_visited = []
    dir = tosave + "/"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    for page_num in range(doc.page_count):
        page = doc.get_page_fonts(page_num)
        for fontinfo in page:

            print(fontinfo)
            print(fontinfo[0])
            print("---")
            xref = fontinfo[0]
            if xref in xref_visited:
                continue
            xref_visited.append(xref)
            name, ext, _, content = doc.extract_font(xref)
            name = name.split("+", 1)[1] if "+" in name else name
            if ext != "n/a":
                ofile = open(dir + name + "." + ext, "wb")
                ofile.write(content)
                ofile.close()
    doc.close()
