#!/usr/bin/env python3
"""
Module for making request for Redis
"""
import redis
import requests


r = redis.Redis(host='localhost', port=6379, db=0)


def get_page(url: str) -> str:
    """
    Get_page function
    """
    """obtain the HTML content of a particular URL and returns it.
    """
    response = requests.get(url)
    html_content = response.text
    cached = r.get(f"cached{html_content}")
    if cached:
        return cached.decode("utf-8")
    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10, html_content)
    return html_content
