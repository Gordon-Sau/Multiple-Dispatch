# https://en.wikipedia.org/wiki/Multiple_dispatch
# https://stackoverflow.com/a/4641463
# https://www.artima.com/weblogs/viewpost.jsp?thread=101605
# improves time complexity and makes the behaviour predictable

from .multimethod_trie import __MultiMethodDict

__registry: dict = {}

def multimethod(*args):
    types = args
    def register(function):
        nonlocal types
        name = function.__name__
        mm = __registry.get(name)
        if mm is None:
            mm = __registry[name] = __MultiMethodDict()
        
        if len(types) == 0:
            code = function.__code__
            types = tuple(function.__annotations__.get(arg, object) for arg in 
                (code.co_varnames[i] for i in range(code.co_argcount)))
        elif len(types) == 1 and types[0] is None:
            types = ()
        
        mm.register(types, function)
        return mm
    return register

def mm(func):
    return multimethod()(func)
