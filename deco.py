"""
deco.py

A library of useful Python function decorators.

Decorators allow you to modify the behavior of a function without changing its
code. This can be useful for adding functionality, enforcing constraints, or
modifying how the function is called.

Examples:
"""
from typing import Callable, Dict, List, TypeVar
from functools import wraps

import platform
import threading
import time
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


def retry_on_failure(runs: int) -> Callable[[Callable], Callable]:
    """A decorator that retries a function on failure the specified number of
    times.

    Args:
    - runs: The number of times to retry the function on failure.

    Returns:
    - The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(runs):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == runs - 1:
                        raise
        return wrapper
    return decorator

def unsupported_os(unsupported_os_list: List[str]) -> Callable[[Callable], Callable]:
    """A decorator that checks the current operating system and raises an
    exception if it is in the list of unsupported OSs. Typically you would
    decorate the 'main' function with this.

    Args:
    - unsupported_os_list: A list of strings representing the unsupported operating systems.

    Returns:
    - The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_os = platform.system()
            if current_os in unsupported_os_list:
                raise Exception(f"The current OS ({current_os}) is not supported")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def add_spinner(func: Callable) -> Callable:
    """A decorator that adds a loading spinner while a function is running.

    Args:
    - func: The function to be decorated.

    Returns:
    - The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        spinner_stop = False
        def _show_spinner():
            spinner_chars = ["|", "/", "-", "\\"]
            while not spinner_stop:
                for char in spinner_chars:
                    print(char, end="\r")
                    time.sleep(0.1)
        spinner_thread = threading.Thread(target=_show_spinner)
        spinner_thread.start()
        try:
            result = func(*args, **kwargs)
        finally:
            spinner_stop = True
            spinner_thread.join()
        return result
    return wrapper

def color_text(fg_color: str = "cyan", bg_color: str = "yellow") -> Callable[[Callable], Callable]:
    """
    A decorator that colors text with the given foreground and background colors using ANSI escape codes.

    Args:
    - fg_color: The foreground color of the text. Defaults to "cyan".
    - bg_color: The background color of the text. Defaults to "yellow".

    Returns:
    - The decorated function.
    """
    def _get_color_code(color, background=False):
        colors = {
            "black": 30,
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37,
        }
        if background:
            return colors[color] + 10
        return colors[color]
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            fg_code = _get_color_code(fg_color)
            bg_code = _get_color_code(bg_color, background=True)
            colored_text = f"\033[{bg_code};{fg_code}m{f(*args, **kwargs)}\033[0m"
            print(colored_text)
        return wrapper
    return decorator

def singleton(func: Callable) -> Callable:
    """
    A decorator that turns a function into a singleton, meaning it can only be run once.

    Args:
    - f: The function to be decorated.

    Returns:
    - The decorated function.
    """
    class Wrapper:
        def __init__(self, func):
            self.func = func
            self.ran = False

        def __call__(self, *args, **kwargs):
            if self.ran:
                raise Exception("This function has already been run")
            self.ran = True
            return self.func(*args, **kwargs)

    return Wrapper(func)




@singleton
def loopy():
    print("Testing")
    total = 0
    for i in range(10000000):
        total += i
    return "Hello"


loopy()
loopy()
