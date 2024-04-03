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
        url = args[0]
        access_count = f"cahed:{url}"
        r.incr(access_count)
        r.expire(access_count, 10)
        return func(*args, **kwargs)
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
