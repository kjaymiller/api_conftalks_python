from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database()

def jsonify_results(funct):
    def inner(*args, **kwargs):
        f = funct(*args, **kwargs)
        bson_data = dumps(f, json_options=RELAXED_JSON_OPTIONS)
        return json.loads(bson_data)

    return inner
     
@jsonify_results
def get_db_items(collection, **kwargs):
    collection = db[collection]
    if kwargs.get('_id'):
        print(kwargs.get('_id'))
        return collection.find({'_id': ObjectId(kwargs.get('_id'))})
    
    elif kwargs.get('filter'):
        print('filter detected')
        return collection.find(kwargs.get('filter'))

    else: 
        print('returning all')
        return collection.find()


@jsonify_results
def load_db_data(collection, json_obj):
    collection = db[collection]
    print('inserting item')
    return collection.insert_one(json_obj).inserted_id
    
