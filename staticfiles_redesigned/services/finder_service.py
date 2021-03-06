# coding: utf-8

from __future__ import unicode_literals

import os

from django.contrib.staticfiles import finders

class FinderService(object):
    def check_existance(self, logical_path):
        return bool(finders.find(logical_path))

    def find_storage_with_path(self, logical_path):
        for finder in finders.get_finders():
            for path, storage in finder.list([]):
                prefix = getattr(storage, 'prefix') or ''
                path = os.path.join(prefix, path)
                if path == logical_path:
                    return storage
        raise Exception()

    def get_lines_from_asset(self, asset):
        with self.open_asset(asset) as f:
            lines = list(f)
        return lines

    def open_asset(self, asset):
        storage = self.find_storage_with_path(asset.logical_path)
        prefix = getattr(storage, 'prefix') or ''
        path = os.path.relpath(asset.logical_path, prefix)
        return storage.open(path)

    def get_modified_time_from_logical_path(self, logical_path):
        storage = self.find_storage_with_path(logical_path)
        prefix = getattr(storage, 'prefix') or ''
        path = os.path.relpath(logical_path, prefix)
        return storage.modified_time(path)
