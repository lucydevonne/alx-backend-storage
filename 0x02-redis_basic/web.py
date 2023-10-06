import requests
import redis
import json
from functools import wraps

# Create a Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

# Define a decorator for caching
def cache_page(url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a cache key for the URL
            cache_key = f"count:{url}"
            
            # Check if the cache key exists and is not expired
            cached_data = redis_conn.get(cache_key)
            if cached_data:
                result = json.loads(cached_data)
                return result['content']
            
            # If not cached, fetch the page content
            content = func(*args, **kwargs)
            
            # Cache the content with a 10-second expiration time
            redis_conn.setex(cache_key, 10, json.dumps({"content": content}))
            
            return content
        
        return wrapper
    
    return decorator

# Define the get_page function
@cache_page
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch page from {url}"

if __name__ == "__main__":
    # Test the get_page function with caching
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    content = get_page(url)
    print(content)
