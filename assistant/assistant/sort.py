from pathlib import Path
from re import sub
from shutil import move, unpack_archive
from sys import argv

class SortFolder:

    ARCHIVES = {'.ZIP', '.GZ', '.TAR'}
    AUDIO = {'.MP3', '.OGG', '.WAV', '.AMR'}
    DOCUMENTS = {'.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'}
    IMAGES = {'.JPEG', '.PNG', '.JPG', '.SVG'}
    VIDEO = {'.AVI', '.MP4', '.MOV', '.MKV'}
    TRANS_MAP = {ord('а'): 'a', ord('А'): 'A', ord('б'): 'b', ord('Б'): 'B', ord('в'): 'v', ord('В'): 'V', ord('г'): 'g', ord('Г'): 'G',
                ord('д'): 'd', ord('Д'): 'D', ord('е'): 'e', ord('Е'): 'E', ord('ё'): 'e', ord('Ё'): 'E', ord('ж'): 'j', ord('Ж'): 'J',
                ord('з'): 'z', ord('З'): 'Z', ord('и'): 'i', ord('И'): 'I', ord('й'): 'j', ord('Й'): 'J', ord('к'): 'k', ord('К'): 'K',
                ord('л'): 'l', ord('Л'): 'L', ord('м'): 'm', ord('М'): 'M', ord('н'): 'n', ord('Н'): 'N', ord('о'): 'o', ord('О'): 'O',
                ord('п'): 'p', ord('П'): 'P', ord('р'): 'r', ord('Р'): 'R', ord('с'): 's', ord('С'): 'S', ord('т'): 't', ord('Т'): 'T',
                ord('у'): 'u', ord('У'): 'U', ord('ф'): 'f', ord('Ф'): 'F', ord('х'): 'h', ord('Х'): 'H', ord('ц'): 'ts', ord('Ц'): 'TS',
                ord('ч'): 'ch', ord('Ч'): 'CH', ord('ш'): 'sh', ord('Ш'): 'SH', ord('щ'): 'sch', ord('Щ'): 'SCH', ord('ъ'): '', ord('Ъ'): '',
                ord('ы'): 'y', ord('Ы'): 'Y', ord('ь'): '', ord('Ь'): '', ord('э'): 'e', ord('Э'): 'E', ord('ю'): 'yu', ord('Ю'): 'YU',
                ord('я'): 'ya', ord('Я'): 'YA', ord('є'): 'je', ord('Є'): 'JE', ord('і'): 'i', ord('І'): 'I', ord('ї'): 'ji', ord('Ї'): 'JI',
                ord('ґ'): 'g', ord('Ґ'): 'G'}

    type_list = {
        'images': {'.JPEG', '.PNG', '.JPG', '.SVG'},
        'documents': {'.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'},
        'audio': {'.MP3', '.OGG', '.WAV', '.AMR'},
        'video': {'.AVI', '.MP4', '.MOV', '.MKV'},
        'archives': {'.ZIP', '.GZ', '.TAR'}
    }
    file_list = {
        'images': [],
        'documents': [],
        'audio': [],
        'video': [],
        'archives': [],
        'unknown extensions': []
    }
    known_extensions = set()
    unknown_extensions = set()

    def create_folder(self, path: Path, new_folder: str):
        try:
            Path.mkdir(path / new_folder, exist_ok=True)
        except FileExistsError:
            raise FileExistsError(f'Folder "{new_folder}" is exist in folder "{path}"')

    def delete_folder(self, path: Path):
        try:
            path.rmdir()
        except FileNotFoundError:
            raise FileNotFoundError(f'Impossible delete folder "{path.name}" because it is not exist')
        except OSError:
            raise OSError(f'Impossible delete folder "{path.name}" because it is not empty')

    def rename_file(self, file: Path) -> Path:
        file = Path(file)
        name_file = file.name.removesuffix(file.suffix)
        name_file = self.normalize(name_file)
        try:
            file = file.rename(file.parent.joinpath(name_file + file.suffix))
        except FileNotFoundError:
            raise FileNotFoundError(f'Missing file {file} to rename')
        except FileExistsError:
            raise FileExistsError(f'Cannot rename file {file.name} because it already exists in {file.parent}')
        return Path(file)

    def rename_folder(self, folder: Path):
        try:
            folder.rename(folder.parent.joinpath(self.normalize(folder.name)))
        except FileNotFoundError:
            raise FileNotFoundError(f'Unable to rename folder {folder} to a new one {self.normalize(folder.name)}')
        except PermissionError:
            raise PermissionError(f'Access denied for {folder}')

    def folder_handling(self, folder: Path) -> bool:
        this_dir_empty = True
        for ff in folder.iterdir():
            # working with folders
            if ff.is_dir():
                if not (ff.name in {'images', 'documents', 'audio', 'video', 'archives'}):
                    empty_dir = self.folder_handling(ff)
                    if empty_dir:
                        self.delete_folder(ff)
                    else:
                        self.rename_folder(ff)
                        this_dir_empty = False
                else:
                    this_dir_empty = False
            # working with files
            else:
                this_dir_empty = False
                if ff.suffix.upper() in self.type_list['images']:
                    self.work_with_images(ff)
                elif ff.suffix.upper() in self.type_list['video']:
                    self.work_with_video(ff)
                elif ff.suffix.upper() in self.type_list['documents']:
                    self.work_with_documents(ff)
                elif ff.suffix.upper() in self.type_list['audio']:
                    self.work_with_audio(ff)
                elif ff.suffix.upper() in self.type_list['archives']:
                    self.work_with_archives(ff)
                else:
                    self.work_with_other(ff)
        return this_dir_empty

    def move_file(self, file: Path, folder: str):
        file.parent.joinpath(folder).mkdir(exist_ok=True)
        if file.parent.joinpath(folder, file.name).exists():
            print(f'The file {file.name} already exists in the folder {file.parent.joinpath(folder)}')
            return file
        return move(file, file.parent.joinpath(folder))

    def work_with_archives(self, file: Path):
        file = self.rename_file(file)
        self.file_list['archives'].append(file.name)
        suffix_file = file.suffix.removeprefix('.')
        self.known_extensions.add(suffix_file.upper())
        name_folder = file.name.removesuffix(file.suffix)
        path_archives = file.parent.joinpath('archives', name_folder)
        path_archives.mkdir(exist_ok=True, parents=True)
        unpack_archive(file, path_archives)

    def work_with_audio(self, file: Path):
        file = self.move_file(file, 'audio')
        file = self.rename_file(file)
        self.file_list['audio'].append(file.name)
        self.known_extensions.add(file.suffix.removeprefix('.').upper())

    def work_with_documents(self, file: Path):
        file = self.move_file(file, 'documents')
        file = self.rename_file(file)
        self.file_list['documents'].append(file.name)
        self.known_extensions.add(file.suffix.removeprefix('.').upper())

    def work_with_images(self, file: Path):
        file = self.move_file(file, 'images')
        file = self.rename_file(file)
        self.file_list['images'].append(file.name)
        self.known_extensions.add(file.suffix.removeprefix('.').upper())

    def work_with_other(self, file: Path):
        file = self.rename_file(file)
        self.file_list['unknown extensions'].append(file.name)
        self.unknown_extensions.add(file.suffix.removeprefix('.').upper())

    def work_with_video(self, file: Path):
        file = self.move_file(file, 'video')
        file = self.rename_file(file)
        self.file_list['video'].append(file.name)
        self.known_extensions.add(file.suffix.removeprefix('.').upper())

    def normalize(self, string: str) -> str:
        string = string.translate(self.TRANS_MAP)
        return sub(r'\W', '_', string)


    def sort_files(self, work_dir: str = None):

        path = Path.cwd()
        path = Path('D:\\temp')
        if work_dir is not None:
            path = Path(work_dir)

        if path.exists() and path.is_dir:
            self.folder_handling(path)
            return self.output_file_list()
        else:
            return 'The path to the folder is incorrect'

    def output_file_list(self):
        lenght = 120
        result = '=' * (lenght + 3) + '\n'
        result += str('|{:^20}|{:^100}|'.format('Category', 'File')) + '\n'
        result += '=' * (lenght + 3) + '\n'
        for category in self.file_list:
            for file in self.file_list[category]:
                result += str('|{:<20}|{:<100}|'.format(category, file)) + '\n'
            if len(self.file_list[category]) > 0:
                result += '=' * (lenght + 3) + '\n'
        return result
