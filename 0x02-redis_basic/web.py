#!/usr/bin/env python3
""" Module to make requests to a site and save to Redis """

import functools
import redis
import requests
from typing import Callable


def count_requests(function: Callable) -> Callable:
    """Decorator for counting requests and caching responses in Redis"""

    @functools.wraps(function)
    def wrapper(url):  # sourcery skip: use-named-expression
        """Wrapper for decorator"""
        # Create a Redis connection
        client = redis.Redis()
        client.flushdb()

        count_url_key = f"count:{url}"
        client.incr(count_url_key)
        Count = client.get(count_url_key)
        # print out url count
        print("{} was requested {} times\n\n".format(url, Count))
        cached_url_key = f"cached:{url}"
        cached_html = client.get(cached_url_key)

        if cached_html:
            html = cached_html.decode("utf-8")
            client.delete(cached_url_key)
            return html
        else:
            html = function(url)
            client.set(cached_url_key, html, 10)
            return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL using requests"""
    response = requests.get(url)
    return response.text
