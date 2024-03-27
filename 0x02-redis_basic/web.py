#!/usr/bin/env python3
"""
5. Implementing an expiring web cache and tracker
"""

import requests
import redis
from functools import wraps


r = redis.Redis()

def count_accesses(func):
    """
    How many times a URL was accessed
    """
    @wraps(func)
    def wrapper(url):
        count_key = "count:{}".format(url)
        r.incr(count_key)
        return func(url)
    return wrapper

def cache_page(func):
    """
    Cache the page content
    """
    @wraps(func)
    def wrapper(url):
        cache_key = "cache:{}".format(url)

        cached_content = r.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")
        else:
            page_content = func(url)
            r.setex(cache_key, 10, page_content)
            return page_content
        
    return wrapper

@count_accesses
@cache_page
def get_page(url: str) -> str:
    """
    Fetch and return the HTML content of a URL
    """
    response = requests.get(url)
    return response.text
    