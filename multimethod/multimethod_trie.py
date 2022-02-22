class __MultiMethodDict:
    def __init__(self):
        # a trie-like structure
        self.typemap = {}

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args)
        function = self.get(types)
        if function is None:
            raise TypeError("no match")
        return function(*args)

    def get(self, key: tuple):
        length = len(key)

        # depth first search
        def search(mapping, index):
            if index == length:
                return mapping.get(None, None)

            for t in key[index].__mro__:
                if t in mapping:
                    result = search(mapping[t], index + 1)
                    if result is not None:
                        return result
            return None
        return search(self.typemap, 0)


    def create_dict(self, key: tuple, item, index: int):
        value = {None: item}
        length = len(key)
        for i in range(length - 1, index - 1, -1):
            value = {
                key[i]: value
            }
        return value


    def register(self, types: tuple, function):
        length = len(types)
        value = self.typemap
        for i in range(length):
            if types[i] not in value:
                value[types[i]] = self.create_dict(types, function, i + 1)
                return
            value = value[types[i]]

        value[None] = function


    def __repr__(self):
        return self.typemap.__repr__()
