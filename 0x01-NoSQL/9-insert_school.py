#!/usr/bin/env python3
""" Module that inserts a new document in a collection based on kwargs. """
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new school document into the MongoDB collection.

    Args:
        mongo_collection: The collection where the document will be inserted.
        **kwargs: Keyword arguments for the fields and values of the document.

    Returns:
        The ID of the newly inserted document.
    """
    # Insert the document into the collection
    insertions = mongo_collection.insert_one(kwargs)

    # Return the captured inserted ID.
    return insertions.inserted_id

if __name__ == "__main__":
    list_all = __import__('8-all').list_all


    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    new_school_id = insert_school(school_collection, name="UCSF", address="505 Parnassus Ave")
    print("New school created: {}".format(new_school_id))

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('address', "")))
