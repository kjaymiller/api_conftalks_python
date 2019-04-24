from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database()

def get_db_items(collection, **kwargs):
    collection = db[collection]
    if kwargs.get('_id'):
        print(kwargs.get('_id'))
        cursor = collection.find({'_id': ObjectId(kwargs.get('_id'))})
    
    elif kwargs.get('filter'):
        print('filter detected')
        cursor = collection.find(kwargs.get('filter'))

    else: 
        print('returning all')
        cursor = collection.find()

    bson_data = dumps(cursor, json_options=RELAXED_JSON_OPTIONS)
    return json.loads(bson_data)

