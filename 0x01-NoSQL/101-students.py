#!/usr/bin/env python3
"""
Module that returns all students sorted by average score.
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    function that returns all students sorted by average score

    Returns:
        top students
    """
    top_student = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_student


if __name__ == "__main__":
    list_all = __import__('8-all').list_all
    insert_school = __import__('9-insert_school').insert_school

    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    j_students = [
        {'name': "John", 'topics': [{'title': "Algo", 'score': 10.3}, {'title': "C", 'score': 6.2}, {'title': "Python", 'score': 12.1}]},  # noqa
        {'name': "Bob", 'topics': [{'title': "Algo", 'score': 5.4}, {'title': "C", 'score': 4.9}, {'title': "Python", 'score': 7.9}]},  # noqa
        {'name': "Sonia", 'topics': [{'title': "Algo", 'score': 14.8}, {'title': "C", 'score': 8.8}, {'title': "Python", 'score': 15.7}]},  # noqa
        {'name': "Amy", 'topics': [{'title': "Algo", 'score': 9.1}, {'title': "C", 'score': 14.2}, {'title': "Python", 'score': 4.8}]},  # noqa
        {'name': "Julia", 'topics': [{'title': "Algo", 'score': 10.5}, {'title': "C", 'score': 10.2}, {'title': "Python", 'score': 10.1}]}  # noqa
    ]
    for j_student in j_students:
        insert_school(students_collection, **j_student)

    students = list_all(students_collection)
    for student in students:
        print("[{}] {} - {}".format(student.get('_id'), student.get('name'),
                                    student.get('topics')))

    top_students = top_students(students_collection)
    for student in top_students:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'),
                                     student.get('averageScore')))
