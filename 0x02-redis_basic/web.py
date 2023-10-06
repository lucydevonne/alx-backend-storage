#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-lvl Redis instance
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.
        '''
        # Initialize the count to 0 if it doesn't exist
        redis_store.incr(f'count:{url}', amount=0)
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        # Remove the line that resets the count
        redis_store.setex(f'result:{url}', 10, result)
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request. Caching is implemented using Redis.
    '''
    return requests.get(url).text


if __name__ == "__main__":
    # Test the get_page function with caching
    url = "http://google.com"
    content = get_page(url)
    print(content)
