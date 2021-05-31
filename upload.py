import pymongo
from os import listdir, getenv
from dotenv import load_dotenv
from iso639 import languages
load_dotenv()

MONGO_USERNAME = getenv('MONGO_USERNAME')
MONGO_PASSWORD = getenv('MONGO_PASSWORD')
MONGO_CLUSTER_URL = getenv('MONGO_CLUSTER_URL')
MONGO_DATABASE = getenv('MONGO_DATABASE')

client_connection = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DATABASE}?retryWrites=true&w=majority"
client = pymongo.MongoClient(client_connection)
db = client.alpha

language_collection = db.languages


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

# Populate language collection
for language in languages:
    if len(language.alpha2) > 0:
        language_document = Language(language.alpha2, language.name)
        # language_collection.insert_one(language_document.document())

