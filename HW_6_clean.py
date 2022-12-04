import pathlib
import re
import os
import shutil
import sys


files = {'immages': {'.jpeg', '.png', '.jpg', '.svg', '.psd'},
		'video': {'.avi', '.mp4', '.mov', '.mkv'},
		'documents': {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.xls'},
		'music': {'.mp3', '.ogg', '.wav', '.amr'},
		'books': {'fb2', '.epub'},
		'drawings': {'.dwg', '.dxf'},
		'archives': {'.zip', 'tar', 'bztar', 'gztar', 'xztar'},
		'apps': {'.exe', '.msi'}}


TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}


# Функція знаходження дублікатів
def find_duplicate(path):
	duplicate_files = {}
	for pth in path.rglob('*.*'):
		duplicate_files.setdefault(pth.name, []).append(pth)
	duplicate_files = {k: v for k, v in duplicate_files.items() if len(v) > 1}
	return duplicate_files


#Функція перейменування дублікатів
def rename_duplicate(duplicate_files):
	for file_pathes in duplicate_files.values():
		number = len(file_pathes)
		while number > 0:
			for file_path in file_pathes:
				new_file_path = file_path.parent.joinpath(file_path.stem + '_' + str(number) + file_path.suffix)
				os.rename(file_path, new_file_path)
				number -= 1


#Функція нормалізації тексту
def normalize_text(text):
	text = text.translate(TRANS)
	clean_text = re.sub('\W+', '_', text).capitalize()
	return clean_text


#Функція нормалізації імен файлів
def normalize_files_names(path):
	for element in path.rglob('*.*'):
		new_file_name = path.joinpath(normalize_text(element.stem) + element.suffix)
		os.rename(element, new_file_name)
		

#Функція повертає шлях до папки з файлами
def return_path(path):
	path = pathlib.Path(path)
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
				if element.suffix.casefold() in val:
					new_folder_path = path.joinpath(key)
					new_file_path = new_folder_path.joinpath(element.name)
					os.replace(element, new_file_path)


#Функція переміщення файлів з невідомими розширеннями
def replace_unknown_files(path, is_files):
	for element in path.rglob('*.*'):
		if element.is_file():
			if element.suffix.casefold() not in is_files:
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
	path = sys.argv[-1]
	path = return_path(path)
	duplicate_files = find_duplicate(path)
	rename_duplicate(duplicate_files)
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


