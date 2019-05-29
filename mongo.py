from pymongo import (
        MongoClient,
        ReturnDocument,
        ASCENDING,
        DESCENDING,
        )
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database()


def get_db_data(
        *,
        collection: str = None,
        _id: str = None,
        filter_by: str = None,
        order: str = None,
        sort_by: str = None,
        limit: int = None,
        ):
    """Returns one or more Objects from the collection"""

    orders = {'asc': ASCENDING, 'desc': DESCENDING}
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
            response = response.sort(sort_by, order)


    if limit:
            response = response.limit(int(limit))

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
