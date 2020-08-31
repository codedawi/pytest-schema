from functools import wraps
from typing import Any, Callable


def match(exact: bool = True) -> Callable:
    """
    Decorator to help toggle the cls's state to preform
    validation strictly or non-strictly. This will toggle
    the `self._ignore_extra_keys` value based on `exact` param

    Args:
        exact (bool, optional): Whether validated against exact or allow skip keys.
    """
    def _decorator(f: Callable):
        @wraps(f)
        def _wrapper(self, value: Any) -> bool:
            """
            Wraps the cls methods of AssertSchema object to
            toggle the _ignore_extra_keys property.

            Args:
                self (AssertSchema): initialized object of AssertSchema
                value (Any): value to validate against schema class

            Returns:
                bool: binary true or false state of returned value
            """
            # store original configured value 
            original: bool = self._ignore_extra_keys

            # toggle property to opposite of `exact` param 
            self._ignore_extra_keys = not exact 

            try:
                # call method an store result
                response = f(self, value)
            finally:
                # raise any SchemaErrors after toggling cls
                # state back to original value
                self._ignore_extra_keys = original
            
            # determine binary (true or false state)
            return bool(response)  
        return _wrapper
    return _decorator
