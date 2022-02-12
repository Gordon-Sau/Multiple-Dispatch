# https://en.wikipedia.org/wiki/Multiple_dispatch
# https://stackoverflow.com/a/4641463
# https://www.artima.com/weblogs/viewpost.jsp?thread=101605
# improves time complexity and makes the behaviour predictable


registry: dict = {}

class MultiMethod:
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

        if None in value:
            raise TypeError("duplicate registration")
        value[None] = function


    def __repr__(self):
        return self.typemap.__repr__()


def multimethod(*types):

    def register(function):
        nonlocal types
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod()
        
        if len(types) == 1 and types[0] is None:
            code = function.__code__
            types = tuple(function.__annotations__[arg] for arg in 
                (code.co_varnames[i] for i in range(code.co_argcount)))
        
        mm.register(types, function)
        return mm
    return register

defaultmultimethod = multimethod(None)


# examples
@defaultmultimethod
def foo(a: int, b: int):
    return a  + b

@multimethod(object, str)
def foo(a: object, b: str):
    return str(a) + ',' + b 

@multimethod(str, str)
def foo(a, b):
    return a + ' ' + b


def foo(a: object, b: object, c: object):
    return str(a) + str(b) + str(c)
foo = multimethod(None)(foo)

print(registry)
print(foo('one', 'two'))
print(foo(1, 2))
print(foo(set(), 'str'))
print(foo(1, 2, 'three'))

@multimethod(set)
def foo(a):
    return ''.join([str(v) for v in a])

print(foo({1, 2}))
print(foo({0.2}))
