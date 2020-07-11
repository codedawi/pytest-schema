from typing import Any

from pytest_schema.assert_schema import Schema


def schema(value: Any, **kargs) -> Schema:
    """
    Helper to create an Schema class, accepting
    all kargs to configure underlying Schema class.

    Args:
        value (Any): schema value to validation data against
        **kargs: underlying Schema class keyword args

    Returns:
        Schema: initialized and configured class

    Example:
        ✅ assert schema({ "status": int }) == {"status": 404}
        ❌ assert schema({ "status": int }) == {"status": "404"}
        ✅ assert schema({ "status": int }) == {"status": 404, "timestamp": 1594358256}

    """
    return Schema(value, **kargs)


def exact_schema(value: Any) -> Schema:
    """
    Helper to create an Schema class
    with exact match requirements.

    Args:
        value (Any): schema value to validation data against

    Returns:
        Schema: initialized and configured class with exact match requirements

    Example:

        ✅ assert exact\_schema({ "status": int }) == {"status": 404}
        ❌ assert exact\_schema({ "status": int }) == {"status": "404"}
        ❌ assert exact\_schema({ "status": int }) == {"status": 404, "timestamp": 1594358256}

    """
    return schema(value, ignore_extra_keys=False)


def like_schema(value: Any) -> Schema:
    """
    Helper to create an Schema class
    with non exact match requirements.

    Args:
        value (Any): schema value to validation data against

    Returns:
        Schema: initialized and configured class with non exact match requirements

    
    Example:

        ✅ assert like\_schema({ "status": int }) == {"status": 404}
        ❌ assert like\_schema({ "status": int }) == {"status": "404"}
        ✅ assert like\_schema({ "status": int }) == {"status": 404, "timestamp": 1594358256}

    """
    return schema(value, ignore_extra_keys=True)
