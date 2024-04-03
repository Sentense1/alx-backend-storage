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
    obtain the HTML content of a particular URL and returns it.
    """
    response = requests.get(url)
    html_content = response.text
    if html_content and response.status_code == 200:
        r.incr(f"count:{url}")
        r.expire(f"cached:{url}", 10)
    return html_content
