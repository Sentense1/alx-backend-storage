#!/usr/bin/env python3
""" Module that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client.logs
collection = db.nginx


def method_logs():
    """
    Provides some stats about Nginx logs stored in MongoDB

    Returns:
        log_count, stauts_count, and method_count
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    logs_count = collection.count_documents({})

    status_count = collection.count_documents({"method": "GET",
                                              "path": "/status"})

    method_count = {}

    for method in methods:
        method_count[method] = collection.count_documents({"method": method})

    return logs_count, status_count, method_count


if __name__ == "__main__":
    logs_count, status_count, method_count = method_logs()
    print(f"{logs_count} logs")

    print("Methods:")
    for method, count in method_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_count} status check")
