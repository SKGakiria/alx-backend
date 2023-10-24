#!/usr/bin/python3
"""The BaseCaching module"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache class that inherits from BaseCaching"""

    def __init__(self):
        """Initializes the class using the parent class __init__ method"""
        super().__init__()
        self.list = []

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            pass
        else:
            length = len(self.cache_data)
            if length >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                print("DISCARD: {}".format(self.list[0]))
                del self.cache_data[self.list[0]]
                del self.list[0]
            self.list.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key is not None and key in self.cache_data.keys():
            return self.cache_data[key]
        else:
            return None
