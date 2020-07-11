from schema import And, Or, Hook, Use, Optional, Regex, Forbidden, Literal
from pytest_schema.assert_schema import Schema


class Enum(Schema):
    """Simple interface to create Enum like schema."""
    def __init__(self, *value):
        """
        Initialize schema with list or tuple like values.

        Args:
            *values (List[Any]): values in enum.

        Example:

            Enum([0, 1, 1, 2, 3, 5, 8])
            Enum(["red", "blue", "green"])

        """
        if len(value) == 1 and hasattr(value[0], "__iter__"):
            value = [v for v in value[0]]

        super().__init__(value, ignore_extra_keys=False)
