# databaseContext.py

from pymongo import MongoClient

def get_db(uri, dbname):
    client = MongoClient(uri)
    db = client[dbname]
    return db

def get_collection(db, collection_name):
    return db[collection_name]
