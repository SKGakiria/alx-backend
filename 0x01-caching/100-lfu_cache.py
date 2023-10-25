#!/usr/bin/python3
"""The BaseCaching module"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class that inherits from BaseCaching"""

    def __init__(self):
        """Initializes the class using the parent class __init__ method"""
        super().__init__()
        self.frequency = {}
        self.order = []

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            pass
        else:
            length = len(self.cache_data)
            if length >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                mfu = min(self.frequency.values())
                lfu_keys = []
                for key, val in self.frequency.items():
                    if val == mfu:
                        lfu_keys.append(key)
                if len(lfu_keys) > 1:
                    lru_mfu = {}
                    for key in lfu_keys:
                        lru_mfu[key] = self.order.index(key)
                    discard = min(lru_mfu.values())
                    discard = self.order[discard]
                else:
                    discard = lfu_keys[0]

                print("DISCARD: {}".format(discard))
                del self.cache_data[discard]
                del self.order[self.order.index(discard)]
                del self.frequency[discard]

            if key in self.frequency:
                self.frequency[key] += 1
            else:
                self.frequency[key] = 1
            if key in self.order:
                del self.order[self.order.index(key)]
            self.order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key is not None and key in self.cache_data.keys():
            del self.order[self.order.index(key)]
            self.order.append(key)
            self.frequency[key] += 1
            return self.cache_data[key]
        else:
            return None
