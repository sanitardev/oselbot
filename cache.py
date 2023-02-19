import os
import pickle
from functools import wraps

def cache(max_size=250):
    cache = {}
    cache_path = 'cache.pickle'

    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            cache = pickle.load(f)

    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            if str(args) in cache:
                return cache[str(args)]
            result = func(*args)
            if len(pickle.dumps(cache)) > max_size:
                oldest = sorted(cache.keys())[0]
                del cache[oldest]
            cache[str (args)] = result
            with open(cache_path, 'wb') as f:
                pickle.dump(cache, f)
            return result
        return wrapper
    return decorator