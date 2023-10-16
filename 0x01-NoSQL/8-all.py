#!/busr/bin/env python3
# Python function that lists all documents in a collection
"""
function that lists all documents in a collection
"""

from pymongo import MongoClient


def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection.

    Args:
        mongo_collection: Represents the collection to list documents from.

    Returns:
        A list of all documents, otherwise, an empty list if collection is None
    """
    if mongo_collection is None:
        # Return an empty list if the collection is not valid.
        return []
    else:
        # fetch all documents from the collection.
        lists_all = [doc for doc in mongo_collection.find()]
        # Returns the list of collections
        return lists_all


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
