#!/usr/bin/env python3
"""
Module defines a simple caching class that stores data in a Redis cache.
"""

import redis
import uuid
from ctypes import Union


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


    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        Store the provided data in the Redis cache and return the key.

        Args:
            data (str, bytes, int, or float): The data to be stored in cache.

        Returns:
            str: The randomly generated key used to store the data in cache.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
