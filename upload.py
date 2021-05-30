import pymongo
from os import listdir, getenv
from dotenv import load_dotenv

load_dotenv()
MONGO_USERNAME = getenv('MONGO_USERNAME')
MONGO_PASSWORD = getenv('MONGO_PASSWORD')
client_connection =  f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@<cluster-url>/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(client_connection)
db = client.test
