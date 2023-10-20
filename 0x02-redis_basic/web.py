#!/usr/bin/env python3
""" Module to make requests to a site and save to Redis """

from functools import wraps
import redis
import requests
from typing import Callable

# Create a Redis connection
redis_ = redis.Redis()


def count_requests(function: Callable) -> Callable:
    """Decorator for counting requests and caching responses in Redis"""

    @wraps(function)
    def wrapper(url):
        """Wrapper for decorator"""
        count_url_key = f"count:{url}"
        redis_.incr(count_url_key)
        cached_url_key = f"cached:{url}"
        cached_html = redis_.get(cached_url_key)

        if cached_html:
            return cached_html.decode('utf-8')
        else:
            html = function(url)
            redis_.setex(cached_url_key, 10, html)
            return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL using requests"""
    response = requests.get(url)
    return response.text
