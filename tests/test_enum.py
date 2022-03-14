import pytest

from pytest_schema import schema, Enum, SchemaError


@pytest.mark.parametrize(
    "values, expected",
    [
        (["red", "blue", "green"], "red"),
        ([1, 2, 3], 3),
    ],
)
def test_enum_valid(values, expected):
    assert schema(Enum(*values)) == expected


@pytest.mark.parametrize(
    "values, expected",
    [
        (["red", "blue", "green"], "yellow"),
        ([1, 2, 3], 5),
    ],
)
def test_enum_not_valid(values, expected):
    with pytest.raises(SchemaError):
        assert schema(Enum(*values)) == expected
