import pymongo
from os import listdir, getenv
from dotenv import load_dotenv
from iso639 import languages
import re

# captures the alpha2 code of the word-freq file
freq_regex = re.compile('^word-freq-(.+)-(.+).csv')

class Schema:
    def document(self):
        raise NotImplementedError("Implement document getter.")


class Language(Schema):
    number = 0

    def __init__(self, alpha2, name):
        Language.number += 1
        self.alpha2 = alpha2
        self.name = name

    def document(self):
        return {
            "alpha2": self.alpha2,
            "name": self.name
        }

class RankedWord(Schema):
    def __init__(self, rank, translation_id):
        self.rank = rank
        self.translation_id = translation_id

    def document(self):
        return {
            "rank": self.rank,
            "translation": self.translation_id
        }

class Translation(Schema):
    def __init__(self):
        self.trans_map = dict()
    
    def put(self, language, word):
        self.trans_map[language] = word

    def document(self):
        return self.trans_map

class KnowledgeBase(Schema):
    def __init__(self, language, words):
        self.language = language
        self.words = words

    def document(self):
        return {
            "language": self.language,
            "words": self.words
        }

load_dotenv()

MONGO_USERNAME = getenv('MONGO_USERNAME')
MONGO_PASSWORD = getenv('MONGO_PASSWORD')
MONGO_CLUSTER_URL = getenv('MONGO_CLUSTER_URL')
MONGO_DATABASE = getenv('MONGO_DATABASE')

client_connection = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DATABASE}?retryWrites=true&w=majority"
client = pymongo.MongoClient(client_connection)
db = client.alpha

language_collection = db.languages
translation_collection = db.translations
ranked_words_collection = db.ranked_words

# Populate language collection
for language in languages:
    if len(language.alpha2) > 0:
        language_document = Language(language.alpha2, language.name)
        # language_collection.insert_one(language_document.document())


# Populate translations collection
directory_files = listdir('.')

# word frequency files
for directory_file in directory_files:
    regex_match = freq_regex.findall(directory_file)
    # if regex matches
    if len(regex_match) > 0:
        alpha2_code = regex_match[0][0]
        language_name = regex_match[0][1]
        # open word-freq file
        word_freq_file = open(directory_file, 'r')
        word_freq_lines = word_freq_file.readlines()
        word_freq_file.close()
        ranked_words = []
        for word_freq_line in word_freq_lines[1:]:
            ranked_words.append(word_freq_line.split(',')[0])
        # open translation file
        translation_file_name = f"transword-freq-{alpha2_code}-{language_name}.csv"
        translation_file = open(translation_file_name, "r")
        translation_lines = translation_file.read().split('\n')
        translation_file.close()
        translation_grid = []
        num_rows = len(translation_lines[1].split(',')) # num of ranks there are
        num_cols = len(translation_lines) - 1 # num of languages
        print(translation_file_name, 'cols:', num_cols, 'rows:', num_rows)
        trans_objs = []
        for row in range(num_rows):
            rank = 1 + row
            translation_row = []
            trans_obj = Translation()
            for col in range(1, num_cols):
                lang = translation_lines[0].split(',')[col - 1]
                translation = translation_lines[col].split(',')[row]
                trans_obj.put(lang, translation)
            trans_obj.put(alpha2_code, ranked_words[row])
            translation_id = translation_collection.insert_one(trans_obj.document()).inserted_id
            ranked_word = RankedWord(rank, translation_id)
            ranked_word_id = ranked_words_collection.insert_one(ranked_word.document()).inserted_id

        exit()