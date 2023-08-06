import functools
from typing import Callable, Any


def by(func: Callable[[Any], Any], condition: Callable[[Any], bool]):
    def decorator(decorated):
        @functools.wraps(decorated)
        def wrapper(*args, **kwargs):
            if condition(*args, **kwargs):
                func(*args, **kwargs)

            return decorated(*args, **kwargs)
        return wrapper
    return decorator
