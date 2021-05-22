from os import listdir
from googletrans import Translator

# translator object
translator = Translator()

# scrape file names & supported languages
def is_lang_file(file_name):
    return file_name.split("-")[0] == 'word'

dir_files = listdir(".")
language_files = list(filter(is_lang_file, dir_files))
languages = list(
    map(lambda language_file: language_file.split('-')[2], language_files))

for language_file in language_files:
    # open and read file
    lang_file = open(language_file, 'r')
    read_lang_file = lang_file.read()
    words = read_lang_file.split('\n')
    # get top 100 or however many there exist
    top_100_words = list(map(lambda line: line.split(',')[
                         0], words[1:min(101, len(words))]))
    this_language = language_file.split('-')[2]
    other_languages = filter(
        lambda language: language != this_language, languages)
    for language in other_languages:
        res = translator.translate(
            top_100_words, src=this_language, dest=language)
        print(res)
        print('done')
        exit()

    lang_file.close()
