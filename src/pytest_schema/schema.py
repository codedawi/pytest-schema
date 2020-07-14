from functools import wraps
from typing import Any, Callable

from schema import Schema as BaseSchema, SchemaError


class Schema(BaseSchema):
    """
    Extention of BaseSchema class to implement
    method to help using with `assert` in tests.
    """
    def __init__(
        self,
        schema,
        error=None,
        ignore_extra_keys=True,
        name=None,
        description=None,
        as_reference=False
    ):
        super().__init__(
            schema,
            error=error,
            ignore_extra_keys=ignore_extra_keys,
            name=name,
            description=description,
            as_reference=as_reference
        )

    def __eq__(self, value: Any) -> bool:
        """
        Compares Schema against value provided when
        using the `==` comparsion.

        Raises:
            SchemaError: if validation fails based on all params 
            cls was initailzed with.

        Returns:
            True when `value` is validate against schema.
        """
        return bool(self.validate(value))
    
    def __ne__(self, value: Any) -> bool:
        """
        Compares Schema against value provided when
        using the `!=` comparsion.

        Returns:
            True when `value` is **NOT** validate against schema.
        """
        return not self.is_valid(value)

    @match(exact=True)
    def exact(self, value: Any) -> bool:
        """
        Compares Schema against value required it to be an exact match.

        Args:
            value (Any): data to validate against schema class

        Raises:
            SchemaError: if validation fails based with ignore_extra_keys = False

        Returns:
            True when `value` is validate against schema exactly.
        """
        return self.validate(value)
    
    @match(exact=True)
    def not_exact(self, value: Any) -> bool:
        """
        Compares Schema against value required it to be an exact match.

        Args:
            value (Any): data to validate against schema class

        Raises:
            SchemaError: if validation fails based with ignore_extra_keys = False

        Returns:
            True when `value` is **NOT** validate against schema exactly.
        """
        return not self.is_valid(value)

    @match(exact=False)
    def like(self, value: Any) -> bool:
        """
        Compares Schema against value, does **NOT** require it to be an exact match.

        Args:
            value (Any): data to validate against schema class

        Raises:
            SchemaError: if validation fails based with `ignore_extra_keys = True`

        Returns:
            True when `value` is validate against schema.
        """
        return self.validate(value)
        
    @match(exact=False)
    def not_like(self, value: Any) -> bool:
        """
        Compares Schema against value, does **NOT** require it to be an exact match.
        
        Args:
            value (Any): data to validate against schema class

        Raises:
            SchemaError: if validation fails based with `ignore_extra_keys = True`

        Returns:
            True when `value` is **NOT** validate against schema.
        """
        return not self.is_valid(value)
    
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
        def _wrapper(self: Schema, value: Any) -> bool:
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
