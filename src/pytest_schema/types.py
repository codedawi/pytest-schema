from schema import And, Forbidden, Hook, Literal, Optional, Or, Regex, Use


__all__ = [
    "And",
    "Forbidden",
    "Hook",
    "Literal",
    "Optional",
    "Or",
    "Regex",
    "Use",
    "Enum"
]

class Enum(Or):
    """
    Patch interface of `Or` class with plans to expand the
    interface to support different Enum-like workflows.

    TODO: Support List[Any] constructor input
    TODO: Support python Enum constructor input,
        with value or name option.
    """