from typing import Any, List
from schema import Or

from pytest_schema.schema import Schema


def schema(value: Any, **kargs) -> Schema:
    """
    Helper to create an Schema class, accepting all kargs to configure underlying Schema class.

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
        ✅ assert exact_schema({ "status": int }) == {"status": 404}
        ❌ assert exact_schema({ "status": int }) == {"status": "404"}
        ❌ assert exact_schema({ "status": int }) == {"status": 404, "timestamp": 1594358256}
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
        ✅ assert like_schema({ "status": int }) == {"status": 404}
        ❌ assert like_schema({ "status": int }) == {"status": "404"}
        ✅ assert like_schema({ "status": int }) == {"status": 404, "timestamp": 1594358256}
    """
    return schema(value, ignore_extra_keys=True)


def like(value: Any) -> Schema:
    """
    Helper to create an Schema class with non exact match requirements.

    Args:
        value (Any): schema value to validation data against

    Returns:
        Schema: initialized and configured class with non exact match requirements

    Example:
        ✅ assert like({ "status": int }) == {"status": 404}
        ❌ assert like({ "status": int }) == {"status": "404"}
        ✅ assert like({ "status": int }) == {"status": 404, "timestamp": 1594358256}
    """
    return schema(value, ignore_extra_keys=True)


def exact(value: Any) -> Schema:
    """
    Helper to create an Schema class with exact match requirements.

    Args:
        value (Any): schema value to validation data against

    Returns:
        Schema: initialized and configured class with exact match requirements

    Example:
        ✅ assert exact({ "status": int }) == {"status": 404}
        ❌ assert exact({ "status": int }) == {"status": "404"}
        ❌ assert exact({ "status": int }) == {"status": 404, "timestamp": 1594358256}
    """
    return schema(value, ignore_extra_keys=True)