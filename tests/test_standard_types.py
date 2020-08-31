import pytest
from pytest_schema import schema, SchemaError


@pytest.mark.parametrize(
    "value, type_schema",
    [
        ("hi", str),
        (1, int),
        (1.0, float),
        (True, bool),
        ({"hello": "world"}, dict),
        (("hello", "world"), tuple),
        (["hello", "world"], list),
        (lambda k: True, callable),
    ]
)
def test_schema_standard_types(value, type_schema):

    assert schema(type_schema) == value


@pytest.mark.parametrize(
    "value, type_schema",
    [
        ("hi", int),
        (1, str),
        (1.0, int),
        (True, str),
        ({"hello": "world"}, list),
        (("hello", "world"), str),
        (["hello", "world"], str),
        (lambda k: True, None),
    ]
)
def test_schema_notequal_standard_types(value, type_schema):

    assert schema(type_schema) != value


@pytest.mark.parametrize(
    "value, type_schema",
    [
        ("hi", dict),
        (1, bool),
        (1.0, str),
        (True, str),
        ({"hello": "world"}, list),
        (("hello", "world"), list),
        (["hello", "world"], dict),
        (lambda k: True, bool),
    ]
)
def test_schema_notequal_standard_types(value, type_schema):

    with pytest.raises(SchemaError):
        assert schema(type_schema) == value