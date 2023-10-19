#!/usr/bin/env python3
"""
Module defines a simple caching class that stores data in a Redis cache.
"""

import redis
import uuid
from typing import Union, Callable, Optional
import functools


def call_history(method: Callable) -> Callable:
    """
    Decorator function
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):  # soucery skip: avoid-builtin-shadow
        """
        Wrapper function
        """
        key = method.__qualname__

        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        input_data = str(args)

        self._redis.rpush(inputs_key, input_data)

        output = method(self, *args, **kwargs)

        output_data = str(output)

        self._redis.rpush(outputs_key, output_data)

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    A decorator to count the number of times a method is called using Redis.

    Args:
        method (callable): The method to be decorated.

    Returns:
        callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):  # soucery skip: avoid-builtin-shadow
        # Use the qualified name as the key
        key = method.__qualname__
        # Increment the call coun t using the INCR command
        self._redis.incr(key)
        # Call and return the original method
        return method(self, *args, **kwargs)
    # Return the wrapper function
    return wrapper



class Cache:
    """
    A simple caching class that stores data in a Redis cache.
    """
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initialize the Cache instance with a connection to a Redis server.

        Args:
            host (str): The Redis server hostname or IP adddress
            port (int): The Redis server port (default is 6379).
            db (int): The Redis database index (default is 0).
        """
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()


    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the provided data in the Redis cache and return the key.

        Args:
            data (str, bytes, int, or float): The data to be stored in cache.

        Returns:
            str: The randomly generated key used to store the data in cache.
        """
        # Create a unique id,convert to str, save as key
        key = str(uuid.uuid4())
        # Retrieve data from redis cache, set value of key as retrieved data
        self._redis.set(key, data)
        # Return key as a key-pair {key: "data"}
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from the Redis cache.

        Args:
            key (str): The key associated with the data in the cache.
            fn (Callable, optional): A callable function to transform the data.

        Returns:
            Union[str, int, bytes, float]: The retrieved data.
        """
        # Retrieve the key from cache and save to data
        data = self._redis.get(key)
        # Return data if it is None,as same behavior with redis.get()
        if data is None:
            return data
        # Use the fn function/method to convert the data to str/int
        if fn:
            # Pass the data to fn and save to caalable_fn
            callable_fn = fn(data)
            # Retuen the converted data
            return callable_fn
        # fn was not passed to the get method
        else:
            # Return the data none-converted
            return data


    def get_str(self, key: str) -> str:
        """
        Retrieve data as a string from the Redis cache.

        Args:
            key (str): The key associated with the data in the cache.

        Returns:
            String: The retrieved data as a string.
        """
        # convert the key from cache to a str using anonymous func(fn)
        value = self._redis.get(key, fn=lambda d: d.decode("utf-8"))
        # Return the convert string
        return value

    def get_int(self, key: str) -> int:
        """
        Retrieve data as an integer from the Redis cache.

        Args:
            key (str): The key associated with the data in the cache.

        Returns:
            Integer: The retrieved data as an integer.
        """
        # get the key from cache, save as value
        value = self._redis.get(key)
        try:
            # Convert retrieved value to a string, and then an integer
            value = int(value.decode("utf-8"))
        except Exception:
            # Return None if value is none-convertible
            return None
        # Return the converted integer
        return value
