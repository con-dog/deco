"""
deco.py

A library of useful Python function decorators.

Decorators allow you to modify the behavior of a function without changing its
code. This can be useful for adding functionality, enforcing constraints, or
modifying how the function is called.

Examples:
"""
from typing import Callable, Dict, TypeVar

import timeit


T = TypeVar('T')

def speedtest(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that measures the execution time of the decorated function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    Examples:
        @speedtest
        def foo(x, y):
            return x + y

        foo(3, 4)
        # Output: foo took 0.000001 seconds
    """
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()
        print(f'[*] {func.__name__} took {end - start:.6f} seconds')
        return result
    return wrapper

def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """A decorator that adds memoization behavior to a function.

    Args:
        func: The function to be decorated.

    Returns:
        A new function with memoization behavior.
    """
    cache: Dict[tuple, T] = {}

    def wrapper(*args: tuple) -> T:
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def loopy():
    total = 0
    for i in range(100000):
        total += i


loopy()
