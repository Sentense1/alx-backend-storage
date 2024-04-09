#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient
from collections import Counter

client = MongoClient()
nginx_collection = client.logs.nginx


def log_stats():
    """
    Calculate statistics from the nginx logs collection.
    """
    try:
        # Initialize Counter objects to count occurrences of HTTP
        # methods and IP addresses
        methods = Counter()
        IPs = Counter()

        # Define the HTTP methods to include in the statistics
        included_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

        # Initialize a variable to count the number of requests with
        # the path '/status'
        status = 0

        # Retrieve all documents from the nginx collection using a cursor
        cursor = nginx_collection.find()

        # Count the total number of documents in the nginx collection
        count = nginx_collection.count_documents({})

        # Convert the cursor result into a list of documents
        data = list(cursor)

        # Iterate over each document in the data list
        for doc in data:
            # Check if the 'path' field in the document is '/status'
            if doc.get('path') == '/status':
                # Increment the status counter if the condition is met
                status += 1

            # Retrieve the HTTP method from the document
            method = doc.get('method')

            # Check if the method is included in the list of methods to track
            if method in included_methods:
                # Increment the counter for the method
                methods[method] += 1

            # Retrieve the IP address from the document
            ip = doc.get('ip')

            # Increment the counter for the IP address
            IPs[ip] += 1
    # Exception handling block to catch any potential errors
    except Exception as exc:
        # Print the exception message for debugging purposes
        print(exc)
        # Return default values in case of an error
        return included_methods, {}, 0, 0, {}
    return included_methods, methods, count, status, IPs


# Execute the log_stats function only if this script is run
# as the main program
if __name__ == '__main__':
    # Call the log_stats function to calculate statistics
    included_methods, methods, count, status, IPs = log_stats()

    # Print the total number of logs
    print(f'{count} logs')

    # Print the statistics for each HTTP method
    print('Methods:')
    for method in included_methods:
        print(f'\tmethod {method}: {methods[method]}')

    # Print the number of status checks
    print(f'{status} status check')

    # Print the top 10 most common IP addresses and their counts
    print('IPs:')
    sorted_IPs = sorted(IPs.items(), key=lambda item: -item[1])[:10]
    for ip_and_values in sorted_IPs:
        print(f'\t{ip_and_values[0]}: {ip_and_values[1]}')
