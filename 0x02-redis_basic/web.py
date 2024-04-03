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
    def wrapper(url) -> None:
        """
        MAin function wrapper
        """
        r.incr(f'count:{url}')
        result = r.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = func(url)
        r.set(f'count:{url}', 0)
        r.setex(f'result:{url}', 10, result)
        return result
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
