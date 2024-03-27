#!/usr/bin/env python3
"""
TASKS:
    0. Writing strings to Redis
    1. Reading from Redis and recovering original type
    2. Incrementing values
    3. Storing lists
    4. Retrieving lists
"""

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Counts how many times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_name = method.__qualname__
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Stores the hisory of inputs and outputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


class Cache:
    """
    Cache Class
    """

    def __init__(self):
        """
        Initializes a new cache instances
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a given data
        """
        key = str(uuid.uuid4())
        self._redis.set(name=key, value=data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None) -> Any:
        """
        Retrieves ata from Redis
        """
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)

        return value

    def get_str(self, key: str) ->Optional[str]:
        """
        Retrieves a str value for a given key
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves a int value for a given key
        """
        value = self.get(key)
        return int(value) if value is not None else None

def replay(method: Callable):
    """
    Displays the history of calls
    """
    qualified_name = method.__qualname__
    redis_instance = method.__self__._redis

    count = redis_instance.get(qualified_name)
    if count:
        count = count.decode("utf-8")
    else:
        count = 0

    inputs = redis_instance.lrange("{}:inputs".format(qualified_name), 0, -1)
    outputs = redis_instance.lrange("{}:outputs".format(qualified_name), 0, -1)

    print("{} was called {} times:".format(qualified_name, count))

    for input_val, output_val in zip(inputs, outputs):
        input_str = input_val.decode("utf-8")
        output_str = output_val.decode("utf-8")
        print("{}{} -> {}".format(qualified_name, input_str, output_str))
        