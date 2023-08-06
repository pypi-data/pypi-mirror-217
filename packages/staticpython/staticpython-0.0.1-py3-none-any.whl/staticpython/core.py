from functools import wraps
from typing import get_type_hints

def statictype(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        arg_names = func.__code__.co_varnames
        
        # Check positional arguments
        for name, value in zip(arg_names, args):
            expected_type = hints.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f"Argument '{name}' must be of type '{expected_type.__name__}', not '{type(value).__name__}'")

        # Check keyword arguments
        for name, value in kwargs.items():
            expected_type = hints.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f"Argument '{name}' must be of type '{expected_type.__name__}', not '{type(value).__name__}'")
        
        return func(*args, **kwargs)
    return wrapper
