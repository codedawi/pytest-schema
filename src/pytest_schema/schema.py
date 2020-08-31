from typing import Any, Callable, Optional

from schema import Schema as BaseSchema, SchemaError
from pytest_schema.match import match

class Schema(BaseSchema):
    """
    Extention of BaseSchema class to implement \
    method to help using with `assert` in tests.
    """
    def __init__(
        self,
        schema: Any,
        error: Optional[str] = None,
        ignore_extra_keys: Optional[bool] = True,
        name: Optional[str] = None,
        description: Optional[str] = None,
        as_reference: Optional[bool] = False
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
            SchemaError: if validation fails based on all params \
                cls was initailzed with.

        Returns:
            True when `value` is validate against schema.
        """
        return bool(self.validate(value))
    
    def __ne__(self, value: Any) -> bool:
        """
        Compares Schema against value provided when using the `!=` comparsion.

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
  