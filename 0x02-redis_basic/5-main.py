#!/usr/bin/env python3
""" Main file """

get_page = __import__('web').get_page

# Define the URL
url = "http://slowwly.robertomurray.co.uk"

# Make a request using the decorated get_page functiion
html_content = get_page(url)

# Print the HTML content
print(html_content)
