# PDF-w-Bg-Txtract

Проект предназначен для извлечения текста из PDF файлов, с которыми плохо справляются решения использующие OCR (сложный фон/структура).
Есть возможность подготовить свой датасет и обучить свою модель CNN.

## Требования

### Версия Python

`python3.8`

### FontForge

`20230101`

### Установить зависимости

```bash
pip install -r requirments.txt
```

## Извлечение текста

Для извлечения текста из PDF-файла нужно скачать модели и в консоли запустить функцию text-extractor

### Модели

#### Дефолтная модель

Ссылка для скачивания моделей: <https://disk.yandex.ru/d/dYH4QCtvCMApVQ>

Скачивать модели по пути `data/models/default_models/.keras`

```
├──pdf-complex-background-text-extraction
│  ├── data
│  │  ├── models
│  │  │  ├── default_models
│  │  │  │  ├── rus_eng.keras
│  │  │  │  ├── rus.keras
│  │  │  │  ├── eng.keras
```

#### Кастомная модель

Пример обучения своей модели в `scripts/train_model.py`

Модели сохраняются по пути

```
├──pdf-complex-background-text-extraction
│  ├── data
│  │  ├── models
│  │  │  ├── custom_models
│  │  │  │  ├── mymodel
│  │  │  │  │  ├── mymodel.keras (weights)
│  │  │  │  │  ├── mymodel.json (labels) 
```

### Пример вызова

Функция использует одну из трёх стандартных моделей

```bash
python text-extractor.py --pdf_path path/to/pdf --model_name ruseng
```

### Параметры

1. `pdf_path`: путь до pdf
2. `model_name`: rus/eng/ruseng

<!-- ## Своя CNN

### Набор данных

Используемый для создания дефолтных моделей [набор шрифтов](https://disk.yandex.ru/d/ck7qBfVkclolRA) и вышедшие из него [датасеты](https://disk.yandex.ru/d/FIKY0vBl2Fv9WQ).

#### Создание датасета

Для создания датасета написан модуль `data_prepare`. Пример использования в `scripts/create_dataset.py`

####

### Обучение

Для работы с CNN написан модуль `model`, пример использования которого для обучения в `scripts/train_model.py` -->

## Набор шрифтов и датасеты

[Набор шрифтов](https://disk.yandex.ru/d/ck7qBfVkclolRA) состоит из шрифтов формата TTF, OTF и из них было подготовлено 3 [датасета](https://disk.yandex.ru/d/FIKY0vBl2Fv9WQ)

#### Пути

##### Набор шрифтов

```
├──pdf-complex-background-text-extraction
│  ├── data
│  │  ├── fonts-folder (Путь с папками, в которых находятся шрифты)
│  │  │  ├── myfonts1
│  │  │  │  ├── font1.ttf
│  │  │  │  ├── font2.otf
│  │  │  │  ├── ...
│  │  │  ├── myfonts2
│  │  │  │  ├── ...
```

##### Путь сохранения датасетов

```
├──pdf-complex-background-text-extraction
│  ├── data
│  │  ├── datasets
│  │  │  ├── mydataset
│  │  │  │  ├── test 
│  │  │  │  ├── train
│  │  │  │  ├── val
```
