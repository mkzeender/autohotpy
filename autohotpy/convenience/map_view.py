from typing import Any, MutableMapping

from autohotpy.proxies.ahk_object import AhkObject


class MapView(MutableMapping):
    """
    A convenient wrapper for an ahk Map object, which provides all the methods
    and properties of the python dictionary. It can also be used to convert
    between a python dict and ahk Map.

    >>> new_dict = MapView(ahk.my_map).to_dict()

    >>> view = MapView(ahk.Map())
    >>> view.update(my_dict)
    >>> my_map = view.map
    """

    def __init__(self, map: AhkObject, **kwargs):
        self.map = map
        self.update(kwargs)

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, item, value):
        self.map[item] = value

    def __delitem__(self, key):
        self.map.delete(key)

    def __contains__(self, key: Any) -> bool:
        return self.map.Has(key)

    def __iter__(self):
        return iter(self.map)

    def __len__(self):
        return self.map.Count

    def get(self, key, default=None):
        return self.map.Get(key, default)

    def clear(self):
        return self.map.clear()

    def copy(self):
        return self.map.clone()

    def to_dict(self):
        return {**self}
