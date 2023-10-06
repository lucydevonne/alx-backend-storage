#!/usr/bin/env python3
""" Expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Create a Redis connection
redis_conn = redis.Redis()

def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator """
        # Use a different key format for caching
        cache_key = f"cached:{url}"

        # Check if the response is cached
        cached_response = redis_conn.get(cache_key)
        if cached_response:
            return cached_response.decode('utf-8')

        # Fetch the page if not cached
        result = fn(url)

        # Cache the response with a 10-second expiration time
        redis_conn.setex(cache_key, 10, result)
        return result

    return wrapper

@wrap_requests
def get_page(url: str) -> str:
    """ Get page content """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # This is just a simple example of using the get_page function
    url = "http://google.com"
    page_content = get_page(url)
    print(page_content)
