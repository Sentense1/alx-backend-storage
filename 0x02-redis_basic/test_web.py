#!/usr/bin/env python3

import time
import web
import redis

# Define the URL to test
url = "http://www.google.com"

# Create a Redis connection
redis_ = redis.Redis()

# Get the count for the URL
count_url_key = f"count:{url}"
initial_count = int(redis_.get(count_url_key) or 0)

# Make a request using the decorated get_page function
html_content = web.get_page(url)

# Print the HTML content
print(f"HTML content for {url}:")
print(html_content)

# Wait for 11 seconds to ensure the cached data expires
time.sleep(11)

# Attempt to retrieve the HTML content again
cached_html = web.get_page(url)

# Print the cached HTML content after waiting
print(f"HTML content for {url} (after waiting):")
print(cached_html)

# Get the updated count for the URL
updated_count = int(redis_.get(count_url_key))

print(f"Initial count for {url}: {initial_count}")
print(f"Updated count for {url}: {updated_count}")

# Check if the count was incremented and if the cached data expired
if initial_count < updated_count:
    print("The count was incremented.")
else:
    print("The count was not incremented.")

if cached_html is None:
    print("The cached data has expired.")
else:
    print("The cached data has not expired.")

