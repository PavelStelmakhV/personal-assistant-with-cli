from pathlib import Path

ARCHIVES = {'.ZIP', '.GZ', '.TAR'}
AUDIO = {'.MP3', '.OGG', '.WAV', '.AMR'}
DOCUMENTS = {'.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'}
IMAGES = {'.JPEG', '.PNG', '.JPG', '.SVG'}
VIDEO = {'.AVI', '.MP4', '.MOV', '.MKV'}

# file_list = {
#     'images': [],
#     'documents': [],
#     'audio': [],
#     'video': [],
#     'archives': [],
#     'unknown extensions': [],
#     'folder': []
# }
# known_extensions = set()
# unknown_extensions = set()


def folder_handling(folder: Path, file_list: dict):
    for file in folder.iterdir():
        if file.is_dir():
            file_list['folder'].append(file.name)
        else:
            if file.suffix.upper() in IMAGES:
                file_list['images'].append(file.name)
            elif file.suffix.upper() in VIDEO:
                file_list['video'].append(file.name)
            elif file.suffix.upper() in DOCUMENTS:
                file_list['documents'].append(file.name)
            elif file.suffix.upper() in AUDIO:
                file_list['audio'].append(file.name)
            elif file.suffix.upper() in ARCHIVES:
                file_list['archives'].append(file.name)
            else:
                file_list['unknown extensions'].append(file.name)


def sort_files(work_dir: str = None):

    file_list = {
        'images': [],
        'documents': [],
        'audio': [],
        'video': [],
        'archives': [],
        'unknown extensions': [],
        'folder': []
    }

    path = Path.cwd()
    if work_dir is not None:
        path = Path(work_dir)

    if path.exists() and path.is_dir:
        folder_handling(path, file_list)
        return output_file_list(file_list)
    else:
        return 'Путь к папке указан не корректно'


def output_file_list(file_list: dict):
    lenght = 120
    result = '=' * (lenght + 3) + '\n'
    result += str('|{:^20}|{:^100}|'.format('Category', 'File')) + '\n'
    result += '=' * (lenght + 3) + '\n'
    for category in file_list:
        for file in file_list[category]:
            result += str('|{:<20}|{:<100}|'.format(category, file)) + '\n'
        if len(file_list[category]) > 0:
            result += '=' * (lenght + 3) + '\n'
    return result
