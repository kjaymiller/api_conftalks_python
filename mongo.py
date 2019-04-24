from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS

import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database()

def get_all_items(collection):
    cursor = db[collection].find()
    return dumps(cursor, json_options=RELAXED_JSON_OPTIONS)

def get_db_object_by_id(collection, object_id):
    cursor = db[collection].find_one({'_id': ObjectId(object_id)})
    return json.dumps(cursor, json_mode=1)
