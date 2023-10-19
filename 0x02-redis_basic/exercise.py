#!/usr/bin/env python3
"""
Module defines a simple caching class that stores data in a Redis cache.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self, key: str, fn: Callable = None):
        """
        Retrieve data from the Redis cache.

        Args:
            key (str): The key associated with the data in the cache.
            fn (Callable, optional): A callable function to transform the data.

        Returns:
            Union[str, int, bytes]: The retrieved data.
        """
        # Retrieve the key from cache and save to data
        data = self._redis.get(key)
        # Return data if it is None,as same behavior with redis.get()
        if data is None:
            return data
        # Use the fn function/method to convert the data to str/int
        callable_fn = fn(data)
        # Return the converted str/int
        return callable_fn


    def get_str(self, key: str) -> Union[str, bytes]:
        """
        Retrieve data as a string from the Redis cache.

        Args:
            key (str): The key associated with the data in the cache.

        Returns:
            Union[str, bytes]: The retrieved data.
        """
        # convert the key from cache to a str using anonymous func(fn)
        value = self._redis.get(key, fn=lambda d: d.decode("utf-8"))
        # Return the convert string
        return value

    def get_int(self, key: str) -> Union[int, bytes]:
        """
        Retrieve data as an integer from the Redis cache.

        Args:
            key (str): The key associated with the data in the cache.

        Returns:
            Union[int, bytes]: The retrieved data as an integer or bytes.
        """
        # convert the key from cache to an int
        value = self._redis.get(key, fn=int)
        # Return the converted integer
        return value


if __name__ == "__main__":
    # create cache instance to store data
    cache = Cache()

    # create data to be stored
    TEST_CASES = {
        # converted to bytes
        b"foo": None,
        # converted to integer
        123: int,
        # converted to string
        "bar": lambda d: d.decode("utf-8")
    }

    # 
    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
