"""
This module provides some examples and shows how multimethod can be used.
"""
from multimethod import multimethod

@multimethod(None)
def foo():
    return 1

@multimethod()
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
foo = multimethod()(foo)

print(foo())
print(foo('one', 'two'))
print(foo(1, 2))
print(foo(set(), 'str'))
print(foo(1, 2, 'three'))

@multimethod(set)
def foo(a):
    return ''.join([str(v) for v in a])

print(foo({1, 2}))
print(foo({0.2}))
