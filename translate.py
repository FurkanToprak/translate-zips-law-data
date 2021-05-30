from os import listdir, getenv, environ
from google.cloud import translate
from dotenv import load_dotenv

load_dotenv()
environ["GOOGLE_APPLICATION_CREDENTIALS"]= getenv('GOOGLE_AUTH_JSON_PATH')

auth_project_id = getenv('PROJECT_ID')

parent = f"projects/{auth_project_id}"
client = translate.TranslationServiceClient()


def translate_text(target_language_code, texts):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    response = client.translate_text(
        contents=texts,
        target_language_code=target_language_code,
        parent=parent,
    )
    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    return translations


# scrape file names & supported languages
n = 300

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
    # get top n or however many there exist
    top_n_words = list(map(lambda line: line.split(',')[
                         0], words[1:min(1 + n, len(words))]))
    this_language = language_file.split('-')[2]
    other_languages = list(filter(
        lambda language: language != this_language, languages))

    # open output file
    trans_lang_file = open('trans' + language_file, 'w')
    trans_lang_file.write(','.join(other_languages));
    trans_lang_file.write('\n')
    for target_language in other_languages:
        cache_translations = translate_text(target_language, top_n_words)
        cache_string = ",".join(cache_translations)
        trans_lang_file.write(cache_string)
        trans_lang_file.write('\n')
    trans_lang_file.close()
    lang_file.close()
