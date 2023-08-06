#!/usr/bin/python3
# -*- coding: utf-8 -*-

import errno
import types
import typing as t

from os import path

__all__ = ("Config",)


class Config(dict):
    """Works exactly like a dict but provides ways to fill it from files
    or special dictionaries. There are two common patterns to populate the
    config: from_py_file or from_object"""

    def __init__(self, root_path=None, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path
        if self.root_path is None:
            self.root_path = path.dirname(path.realpath(__file__))
        elif path.isfile(self.root_path):
            self.root_path = path.dirname(path.realpath(self.root_path))

    def from_py_file(self, filename, silent=False):
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the `from_object` function.

        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.
        """
        filename = path.join(self.root_path, filename)
        d = types.ModuleType("config")
        d.__file__ = filename
        try:
            with open(filename, mode="rb") as config_file:
                exec(compile(config_file.read(), filename, "exec"), d.__dict__)
        except IOError as err:
            if silent and err.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
                return False
            err.strerror = f"Unable to load configuration file ({err.strerror})"
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        """
        Updates the values from the given object.

        :param obj: an import name or object
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def get_namespace(self, namespace: str, lowercase: bool = True, trim_namespace: bool = True) -> t.Dict[str, t.Any]:
        """Returns a dictionary containing a subset of configuration options
        that match the specified namespace/prefix. Example usage::

            app.config['IMAGE_STORE_TYPE'] = 'fs'
            app.config['IMAGE_STORE_PATH'] = '/var/app/images'
            app.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'
            image_store_config = app.config.get_namespace('IMAGE_STORE_')

        The resulting dictionary `image_store_config` would look like::

            {
                'type': 'fs',
                'path': '/var/app/images',
                'base_url': 'http://img.website.com'
            }

        This is often useful when configuration options map directly to
        keyword arguments in functions or class constructors.

        :param namespace: a configuration namespace
        :param lowercase: a flag indicating if the keys of the resulting
                          dictionary should be lowercase
        :param trim_namespace: a flag indicating if the keys of the resulting
                          dictionary should not include the namespace

        """
        rv = {}
        for k, v in self.items():
            if not k.startswith(namespace):
                continue
            key = k[len(namespace) :] if trim_namespace else k
            if lowercase:
                key = key.lower()
            rv[key] = v
        return rv

    def from_mapping(self, mapping: t.Optional[t.Mapping[str, t.Any]] = None, **kwargs: t.Any) -> bool:
        """
        Updates the config like :meth:`update` ignoring items with non-upper keys.

        :return: Always returns ``True``.
        """
        mappings: t.Dict[str, t.Any] = {}
        if mapping is not None:
            mappings.update(mapping)
        mappings.update(kwargs)
        for key, value in mappings.items():
            if key.isupper():
                self[key] = value
        return True
