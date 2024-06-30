#!/usr/bin/env python3
"""
Module for making request for Redis
"""
import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis(host='localhost', port=6379, db=0)


def counter(func: Callable) -> Callable:
    """
    FUnction wrapper, outer
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> None:
        """
        MAin function wrapper
        """
        key = f"count:{args[0]}"
        if r.get(key):
            r.incr(key)
            # print('ttl: ', r.ttl(key))
            # print('key: ', r.get(key))
            r.expire(key, 10)
        else:
            r.setex(key, 10, 1)
        result = func(*args, **kwargs)
        # print('cached value: ', r.get(key))
        return result
    wrapper.__qualname__ = func.__qualname__
    return wrapper


@counter
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using requests.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    html_content = response.text
    return html_content


if __name__ == '__main__':
    get_page('http://slowwly.robertomurray.co.uk')
