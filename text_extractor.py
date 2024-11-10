import argparse
from pdf_worker.pdf_reader import PDFReader
from pathlib import Path


def main(pdf_path: Path, model_name: str):
    reader = PDFReader.load_default_model(model_name)
    text = reader.restore_text(pdf_path)
    print(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Выбор модели для извлечения текста и путь до PDF файла")
    parser.add_argument("pdf_path", help="Путь до PDF файла")
    parser.add_argument("model_name", help="Модель: rus, eng, ruseng")
    args = parser.parse_args()
    main(args.pdf_path, args.model_name)
