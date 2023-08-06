# src/func_cache.py
# Caches the return values of a function


# Imports
from __future__ import annotations

import hashlib
from functools import partial
from threading import Thread
from typing import Any, Callable


# Metadata
__all__ = ["func_cache", "thread_wrap"]


# Definitions
def func_cache() -> Callable:
    """
    ### Summary
    A decorator for caching function return values.  
    Caches based on function arguments.  
    This can be useful for functions that will return the same value each time for given arguments, but for whatever reason, may not be ideal to run more than once.
    
    ### Returns
    Callable # The decorator
    
    ### Usage:
    >>> from naters_utils.functions import func_cache
    >>> @func_cache()
    ... def some_repetitive_function(arg):
    ...     # Some code
    ...
    >>> some_repetitive_function(1)
    Some result
    >>> some_repetitive_function(1)
    The same result
    """
    
    def decorator(func: Callable) -> Callable:
        """The decorator itself"""
        
        class Wrapper:
            """The wrapper itself"""

            def __init__(self, func: callable) -> None:
                """Create the wrapper"""

                # Set variables
                self._func = func
                self._cache = {}


            def __call__(self, *args, **kwargs) -> Any:
                """Run the function and cache, or return cached value"""
                
                try:
                    out = self._cache[hashlib.new("sha1", str({"args": args, "kwargs": kwargs}).encode()).hexdigest()]
                except KeyError:
                    out = self._func(*args, **kwargs)
                    self._cache[hashlib.new("sha1", str({"args": args, "kwargs": kwargs}).encode()).hexdigest()] = out
                
                return out
            
            def __get__(self, instance, owner) -> partial:
                """Compatibility with objects"""
                
                return partial(self, instance)
        
        return Wrapper(func)
    
    return decorator


def thread_wrap(thread_name: str) -> Callable:
    """
    ### Summary
    A decorator for turning a function into a thread.  
    Just decorate the function and run it like normal!  
    This is useful for functions that can take a long time to run, but don't need to be run in series with the rest of the code.
    
    ### Parameters:
        thread_name: str # The name of the thread that is created
    
    ### Returns:
        Callable # The decorator
    
    ### Usage:
    >>> from naters_utils.functions import thread_wrap
    >>> @thread_wrap()
    ... def some_long_function():
    ...     # Some code
    ...
    >>> some_long_function()
    >>> print("I can still run")
    I can still run
    """
    
    def decorator(func: Callable) -> Callable:
        """The decorator itself"""
        
        class Wrapper(Thread):
            """The wrapper itself"""

            def __init__(self, func: Callable) -> None:
                """Create the wrapper"""

                # Set variables
                self._func = func
                self._thread_name = thread_name


            def __call__(self, *args, **kwargs) -> Any:
                """Start the thread when called"""

                # Initialize the thread
                super().__init__(target=self._func, name=self._thread_name, args=args, kwargs=kwargs)

                # Start the thread
                self.start()
            
            
            def __get__(self, instance, owner) -> partial:
                """Compatibility with objects"""
                
                return partial(self.__call__, instance)
        
        return Wrapper(func)
    
    return decorator