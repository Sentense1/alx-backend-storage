#!/usr/bin/env python3
'''Module that provides some stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient
from collections import Counter

client = MongoClient()
nginx_collection = client.logs.nginx


def log_stats():
    """
    Calculate statistics from the nginx logs collection.
    """
    try:
        # Counter to store the count of each HTTP method
        methods = Counter()
        # Define the HTTP methods to include in the statistics
        included_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        # Counter to store the count of status check requests
        status = 0

        # Retrieve all documents from the nginx collection
        cursor = nginx_collection.find()
        # Count the total number of documents in the collection
        count = nginx_collection.count_documents({})

        # convert the cursir object to a list
        data = list(cursor)
        # Iterate over each document in the cursor
        for doc in data:
            # Check if the path is '/status' to count status check requests
            if doc.get('path') == '/status':
                status += 1
            # Get the HTTP method from the document
            method = doc.get('method')
            # Increment the count for the method if it's included in the
            # specified methods
            if method in included_methods:
                methods[method] += 1
    except Exception as exc:
        # Handle any exceptions and return default values
        print(exc)
        return included_methods, {}, 0, 0

    # Return the included methods, method counts, total log count,
    # and status check count
    return included_methods, methods, count, status


if __name__ == '__main__':
    # Call the log_stats function when the script is executed
    included_methods, methods, count, status = log_stats()

    # Print the total log count
    print(f'{count} logs')
    # Print the count of each HTTP method
    print('Methods:')
    for method in included_methods:
        print(f'\tmethod {method}: {methods[method]}')
    # Print the count of status check requests
    print(f'{status} status check')
