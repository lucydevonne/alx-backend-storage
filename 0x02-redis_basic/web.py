#!/usr/bin/env python3
"""track page visits and cache"""
from functools import wraps
from redis import Redis
import requests
from typing import Callable


url_arg = 'http://slowwly.robertomurray.co.uk'
redis_cli = Redis()


def track_access(func: Callable):
    """Decorator function to track url access"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function"""
        url_key = "count:{}".format(*args)
        incr_val = redis_cli.incr(url_key, 1)
        redis_cli.set(url_key, incr_val, ex=10, xx=True)
        # print(incr_val)
        return func(args, **kwargs)
    return wrapper


@track_access
def get_page(url: str) -> str:
    """retrieve url page"""
    try:
        req = requests.get(url)
        return req.text
    except Exception:
        return ""
