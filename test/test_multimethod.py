from multimethod import *
from multimethod.registry import __registry
import pytest

@pytest.fixture
def clear_registry():
    __registry.clear()

def test_simple_register_success(clear_registry):
    @multimethod(str, str)
    def foo(a, b):
        return 2
    assert foo('a', 'b') == 2

def test_simple_register_exception(clear_registry):
    @multimethod(str, str)
    def foo(a, b):
        return 2
    with pytest.raises(TypeError):
        foo(1, 2)

def test_register_NoneType(clear_registry):
    @multimethod(type(None))
    def foo(null):
        return 1
    assert foo(None) == 1

def test_register_empty(clear_registry):
    @multimethod(None)
    def foo():
        return 0
    assert foo() == 0

def test_register_type_notation(clear_registry):
    @multimethod()
    def foo(a: str, b: str):
        return a + b
    assert foo('hello, ', 'world') == 'hello, world'

def test_multiple_register_no_inheritance(clear_registry):
    @mm
    def foo(a: int, b: int):
        return 0
    
    @mm
    def foo(a: int, b: str):
        return 1

    @mm
    def foo(a: str, b: str):
        return 2
    
    assert foo(1, 2) == 0
    assert foo(1, 'a') == 1
    assert foo('a', 'b') == 2
    with pytest.raises(TypeError):
        foo('a', 1)

def test_different_order(clear_registry):
    @mm
    def foo(a: int, b: int, c: str):
        return 1
    
    @mm
    def foo(a: int, b: str, c: int):
        return 2

    @mm
    def foo(a: str, b: int, c: int):
        return 3

    assert foo(1, 2, 'a') == 1
    assert foo(1, 'a', 2) == 2
    assert foo('a', 1, 2) == 3

def test_different_size(clear_registry):
    @mm
    def foo(a: int, b: int):
        return a + b
    
    @mm
    def foo(a: int, b: int, c: int):
        return a + b + c
    
    @mm
    def foo():
        return 0
    
    assert foo(1, 2) == 3
    assert foo(2, 3, 4) == 9
    assert foo() == 0
    with pytest.raises(TypeError):
        foo(1, 2, "hi")
    with pytest.raises(TypeError):
        foo('a', 1, 2)


def test_simple_inheritance(clear_registry):
    @mm
    def foo(a: int):
        return 1

    @mm
    def foo(b: object):
        return 0


    # https://stackoverflow.com/a/37888668
    # For historic reasons, bool is a subclass of int
    @mm
    def foo(c: bool):
        return 2

    class IntChlid(int):
        def __init__(self) -> None:
            super().__init__()

    class IntGrandchild(IntChlid):
        def __init__(self) -> None:
            super().__init__()
    
    assert foo(1) == 1
    assert foo(0.1) == 0
    assert foo(False) == 2
    assert foo(IntChlid()) == 1
    assert foo(IntGrandchild()) == 1

    @mm
    def foo(x: IntChlid):
        return 3
    assert foo(IntChlid()) == 3
    assert foo(IntGrandchild()) == 3

    @mm
    def foo(y: IntGrandchild):
        return 4
    assert foo(IntChlid()) == 3
    assert foo(IntGrandchild()) == 4

def test_more_inheritance(clear_registry):
    @mm
    def foo(a: object, b: str):
        return 0

    @mm
    def foo(a: str, b: str):
        return 1
    
    class StrChild(str):
        def __init__(self) -> None:
            super().__init__()

    @mm
    def foo(a: str, b: object):
        return 2

    @mm
    def foo(a: StrChild, b: object):
        return 3

    assert foo(1, 'a') == 0
    assert foo('a', 'b') == 1
    assert foo('a', StrChild()) == 1
    assert foo(StrChild(), StrChild()) == 3

    @mm
    def foo(a: str, b: StrChild):
        return 4
    
    assert foo('a', StrChild()) == 4
    assert foo(StrChild(), StrChild()) == 3

def test_mm_no_annotation():
    @mm
    def foo(a, b):
        return 0
    assert foo(object(), object()) == 0
