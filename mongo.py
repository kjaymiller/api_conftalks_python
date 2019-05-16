from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database()


def jsonify(funct):
    def inner(*args, **kwargs):
        f = funct(*args, **kwargs)

        if kwargs.get('sort'):
            f = f.sort(kwargs['sort'])

        if kwargs.get('limit'):
            f = f.limit(kwargs['limit']) 

        bson_data = dumps(f, json_options=RELAXED_JSON_OPTIONS)
        bson_data['id'] = bson_data['id']['$oid'] 
        return json.loads(bson_data)
    return inner


@jsonify
def get_db_data(collection, _id=False, filter_by=False, return_one=False,
        **kwargs):
    collection = db[collection]

    if _id:
        response = collection.find_one({'_id': ObjectId(_id)}, **kwargs)

    elif filter_by and return_one:
        response = collection.find_one(filter_by, **kwargs)

    elif filter_by:
        response = collection.find(filter_by, **kwargs)

    else: 
        response = collection.find({}, **kwargs)

    return response

@jsonify
def update_db_data(collection, data, _id=False, filter_by=None, **kwargs):
    collection = db[collection]
    if _id:
        filter = {'_id': ObjectId(_id)}

    else:
        filter = filter_by

    return collection.find_one_and_update(
            filter, 
            data, 
            return_document=ReturnDocument.AFTER,
            **kwargs)
        

@jsonify
def load_db_data(collection, json_obj):
    collection = db[collection]
    return collection.insert_one(json_obj).inserted_id
