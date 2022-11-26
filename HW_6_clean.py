import pathlib
import re
import os
import shutil


files = {'immages': {'.jpeg', '.png', '.jpg', '.svg', '.psd'},
		'video': {'.avi', '.mp4', '.mov', '.mkv'},
		'documents': {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.xls'},
		'music': {'.mp3', '.ogg', '.wav', '.amr'},
		'books': {'fb2', '.epub'},
		'drawings': {'.dwg', '.dxf'},
		'archives': {'.zip', 'tar', 'bztar', 'gztar', 'xztar'},
		'apps': {'.exe', '.msi'}}


#Функція нормалізації тексту
def normalize_text(text):
	clean_text = re.sub('\W+', '_', text).capitalize()
	return clean_text


#Функція нормалізації імен файлів
def normalize_files_names(path):
	for element in path.rglob('*.*'):
		new_file_name = path.joinpath(normalize_text(element.stem) + element.suffix)
		os.rename(element, new_file_name)
		

#Функція повертає шлях до папки з файлами
def return_path():
	path = pathlib.Path(input('Insert path: '))
	if path.exists():
		return path
	else:
		print(f'path {path.absolute()} not exists')


#Функція створення та заповнення масивів
def arrays_filling(path):
	files_extension = set()
	files_path = []
	files_name = []
	is_files = set()
	not_files = set()
	for element in path.rglob('*.*'):
		if element.is_file():
			files_extension.add(element.suffix)
			files_path.append(element)
			files_name.append(element.name)
			for key, val in files.items():
				if element.suffix in val:
					is_files.add(element.suffix)
			if element.suffix not in is_files:
				not_files.add(element.suffix)
	return [files_extension, files_path, files_name, is_files, not_files]


#Функція створення папок по категоріям
def making_dir(path, files_extension):
	other_folder_path = path.joinpath('other')
	other_folder_path.mkdir(exist_ok=True)
	for key, val in files.items():
		if val & files_extension:
			folder_path = path.joinpath(key)
			folder_path.mkdir(exist_ok=True)


#Функція переміщення файлів з відомими розширеннями
def replace_known_files(path):
	for element in path.rglob('*.*'):
		if element.is_file():
			for key, val in files.items():
				if element.suffix in val:
					new_folder_path = path.joinpath(key)
					new_file_path = new_folder_path.joinpath(element.name)
					os.replace(element, new_file_path)


#Функція переміщення файлів з невідомими розширеннями
def replace_unknown_files(path, is_files):
	for element in path.rglob('*.*'):
		if element.is_file():
			if element.suffix not in is_files:
				other_folder_path = path.joinpath('other')
				other_file_path = other_folder_path.joinpath(element.name)
				os.replace(element, other_file_path)


#Функція разархівування
def unpacking_archives(path):
	archives_path = path.joinpath('archives')
	for element in archives_path.glob('*.*'):
		archive_files_path = archives_path.joinpath(element.stem)
		shutil.unpack_archive(str(element), str(archive_files_path))


#Функція видалення пустих папок
def remove_directories(path):
    for directories in os.listdir(path):
        dir_path = os.path.join(path, directories)
        if os.path.isdir(dir_path):
            remove_directories(dir_path)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def main():
	path = return_path()
	normalize_files_names(path)
	arrays_filling(path)
	files_extension = arrays_filling(path)[0]
	is_files = arrays_filling(path)[3]
	making_dir(path, files_extension)
	replace_known_files(path)
	replace_unknown_files(path, is_files)
	unpacking_archives(path)
	remove_directories(path)
	print('Everything is cleaned!')



if __name__ == '__main__':
	main()


