#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import StorageServer2
except Exception:
    import storageserverdummy as StorageServer2


class CacheFunc():

    def __init__(self):
        self.storageStack = {}

    def get_cache_data(self, data_type, key=None, time=5):
        if data_type in self.storageStack:
            cache = self.storageStack[data_type]
        else:
            cache = StorageServer2.TimedStorage(data_type, time)
            self.storageStack[data_type] = cache
        if key is None:
            key = data_type
        try:
            _data = cache[key]
            print "-------GOT CACHE--------TYPE:" + data_type + " KEY:" + str(key)
            return _data
        except Exception:
            print "--Error--GOT CACHE--------TYPE:" + data_type + " KEY:" + str(key)
            return None

    def set_cache_data(self, data_type, data, key=None, time=5):
        if data_type in self.storageStack:
            cache = self.storageStack[data_type]
        else:
            cache = StorageServer2.TimedStorage(data_type, time)
            self.storageStack[data_type] = cache
        if key is None:
            key = data_type
        cache[key] = data
