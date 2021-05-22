from os import listdir

dir_files = listdir(".")


def is_lang_file(file_name):
    return file_name.split("-")[0] == 'word'


language_files = filter(is_lang_file, dir_files)

for language_file in language_files:
    print(language_file)