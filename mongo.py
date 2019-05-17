from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database()


def jsonify(schema):
    def decorator(funct):
        def inner(**kwargs):
            f = funct(**kwargs)
            bson_data = dumps(f, json_options=RELAXED_JSON_OPTIONS)
            schema = kwargs['schema']
            bson_data = json.loads(bson_data)
            return schema.dump(bson_data)
        return inner
    return decorator


def get_db_data(
        *, 
        schema = None, 
        collection: str = None, 
        _id: str = '', 
        filter_by: dict = {},
        return_one: bool = False,
        sort = None,
        limit = None, 
        ):
    """Returns one or more Objects from the collection"""

    collection = db[collection]

    if _id:
        response = collection.find_one({'_id': ObjectId(_id)})

    elif filter_by and return_one:
        response = collection.find_one(filter_by)

    elif filter_by:
        response = collection.find(filter_by)

    else: 
        response = collection.find({})

    
    if sort:
            response = response.sort(sort)

    if limit:
            response = response.limit(limit)

    return response

def update_db_data(
        *, 
        schema = None, 
        collection: str = None, 
        _id: str = '', 
        filter_by: dict = {},
        return_one: bool = False,
        sort = None,
        limit = None, 
        ):

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
        

def load_db_data(
        *, 
        schema = None, 
        collection: str = None, 
        _id: str = '', 
        filter_by: dict = {},
        return_one: bool = False,
        sort = None,
        limit = None, 
        ):

    collection = db[collection]
    return collection.insert_one(json_obj).inserted_id
