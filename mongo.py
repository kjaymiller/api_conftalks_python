from pymongo import MongoClient
from config import (
        MLAB_URL, 
        MLAB_DB,
        )

client = MongoClient(MLAB_URL)
db = client[MLAB_DB]
conferences = db.conferences
