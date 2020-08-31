import pytest

from pytest_schema import SchemaError, schema


@pytest.mark.parametrize(
    "value, basic_schema",
    [
        (
            {"id": 1, "username": "helloworld"},
            {
                "id": int,
                "username": str,
            },
        ),
        ({"hello": {"hey": "world"}}, {"hello": dict}),
    ],
)
def test_schema_basic_dicts(value, basic_schema):

    assert schema(basic_schema) == value
