import sys


def sorting():
    try:
        target_folder = sys.argv[1]
    except IndexError:
        print("Прописати Папку")
        return
    arrange_folder(target_folder)


import os
import shutil
from typing import Dict, List


ARCHIVES = "archives"
UNKNOWN = "unknown"

CATEGORIES: Dict[str, List] = {
    "images": ["jpeg", "png", "jpg", "svg"],
    "videos": ["avi", "mp4", "mov", "mkv"],
    "documents": ["doc", "docx", "txt", "pdf", "xlsx", "pptx"],
    "music": ["mp3", "ogg", "wav", "amr"],
    "archives": ["zip", "gz", "tar"],
    "unknown": [],
}


def define_category(file_path: str):
    global CATEGORIES
    extension = file_path.split(".")[-1]
    for category, category_extensions in CATEGORIES.items():
        if extension in category_extensions:
            return category
    CATEGORIES[UNKNOWN].append(extension)
    return UNKNOWN


def unpack_archive(archive_src: str, destination_folder: str):
    shutil.unpack_archive(archive_src, destination_folder)


def move_to_category_folder(src: str, destination: str):
    category = define_category(src)
    destination_folder: str = os.path.join(destination, category)
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    if category == ARCHIVES:
        unpack_archive(src, destination_folder)
        return
    filename: str = os.path.split(src)[-1]
    new_filename = normalize(filename)
    destination_filepath = os.path.join(destination_folder, new_filename)
    shutil.move(src, destination_filepath)


def arrange_folder(target_path: str, destination_folder: str = None):
    if destination_folder is None:
        destination_folder = target_path
    inner_files = os.listdir(target_path)
    for filename in inner_files:
        file_path: str = os.path.join(target_path, filename)
        if os.path.isdir(file_path):
            arrange_folder(file_path, destination_folder)
        elif os.path.isfile(file_path):
            move_to_category_folder(file_path, destination_folder)
        else:
            raise OSError


import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "u",
    "ja",
    "je",
    "ji",
    "g",
)

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r"\W", "_", t_name)
    return t_name
