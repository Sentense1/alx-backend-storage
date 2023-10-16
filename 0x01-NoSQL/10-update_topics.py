#!/usr/bin/env python3
""" Updates topics of a school document based on the name """

from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """ Update topics for a school document in the MongoDB collection.

    Args:
        mongo_collection: Object representing the collection.
        name: The name of the school document to update.
        topics: The new list of topics to set for the school document.
    """
    query = {"name": name}
    values = {"$set": {"topics": topics}}

    update = mongo_collection.update_many(query, values)


if __name__ == "__main__":
    list_all = __import__('8-all').list_all
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    update_topics(school_collection, "Holberton school",
                  ["Sys admin", "AI", "Algorithm"])

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'),
                                  school.get('topics', "")))

    update_topics(school_collection, "Holberton school", ["iOS"])

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'),
                                  school.get('topics', "")))
