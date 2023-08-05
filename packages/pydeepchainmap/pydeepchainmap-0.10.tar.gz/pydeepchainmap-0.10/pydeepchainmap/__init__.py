from typing import ChainMap


class DeepChainMap(ChainMap):
    """Variant of ChainMap that allows direct updates to inner scopes
    Taken from: https://docs.python.org/3/library/collections.html#collections.ChainMap
    >>> d = DeepChainMap({'zebra': 'black'}, {'elephant': 'blue'}, {'lion': 'yellow'})
    >>> d['lion'] = 'orange'         # update an existing key two levels down
    >>> d['snake'] = 'red'           # new keys get added to the topmost dict
    >>> del d['elephant']            # remove an existing key one level down
    >>> d                            # display result
    DeepChainMap({'zebra': 'black', 'snake': 'red'}, {}, {'lion': 'orange'})
    """

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)
