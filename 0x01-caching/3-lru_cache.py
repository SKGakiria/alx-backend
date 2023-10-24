#!/usr/bin/python3
"""The BaseCaching module"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache class that inherits from BaseCaching"""

    def __init__(self):
        """Initializes the class using the parent class __init__ method"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            pass
        else:
            length = len(self.cache_data)
            if length >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                print("DISCARD: {}".format(self.order[0]))
                del self.cache_data[self.order[0]]
                del self.order[0]
            if key in self.order:
                del self.order[self.order.index(key)]
            self.order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key is not None and key in self.cache_data.keys():
            del self.order[self.order.index(key)]
            self.order.append(key)
            return self.cache_data[key]
        else:
            return None
