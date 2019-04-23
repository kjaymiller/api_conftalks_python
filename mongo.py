from pymongo import MongoClient
from config import MLAB_URL

client = MongoClient(MLAB_URL)
collection = client['conferences']
print(collection)
