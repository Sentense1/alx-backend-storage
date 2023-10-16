#!/usr/bin/env python3
"""  Lists schools by a specific topic in a MongoDB collection. """

from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """ Retrieve schools with a specific topic from the MongoDB collection.

    Args:
        mongo_collection: PyMongo object representing the collection.
        topic: The topic to search for in school documents.

    Returns:
        A list of schools that have the specified topic.
    """
    lists_of_topics = mongo_collection.find({"topics": topic})
    return list(lists_of_topics)


if __name__ == "__main__":
    list_all = __import__('8-all').list_all
    insert_school = __import__('9-insert_school').insert_school
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    j_schools = [
        {'name': "Holberton school", 'topics': ["Algo", "C",
                                                "Python", "React"]},
        {'name': "UCSF", 'topics': ["Algo", "MongoDB"]},
        {'name': "UCLA", 'topics': ["C", "Python"]},
        {'name': "UCSD", 'topics': ["Cassandra"]},
        {'name': "Stanford", 'topics': ["C", "React", "Javascript"]}
    ]
    for j_school in j_schools:
        insert_school(school_collection, **j_school)

    schools = schools_by_topic(school_collection, "Python")
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'),
                                  school.get('topics', "")))
