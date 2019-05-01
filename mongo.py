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
    
    elif kwargs.get('filter_by'):
        print('filter detected')
        return collection.find(kwargs.get('filter_by'))

    else: 
        print('returning all')
        return collection.find()


@jsonify_results
def update_db_data(collection, data, **kwargs):
    print('updating item')
    collection = db[collection]
    if _id:
        return collection.update({'_id': ObjectId(kwargs.get('_id'))}, data)

    else:
        return collection.update(kwargs.get('filter_by'), data)


def load_db_data(collection, json_obj):
    collection = db[collection]
    print('inserting item')
    return collection.insert_one(json_obj).inserted_id
