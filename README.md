# pytest-schema

![](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?logo=python) [![PyPI version](https://img.shields.io/pypi/v/pytest-schema.svg)](https://pypi.python.org/pypi/pytest-schema/) [![PyPI download month](https://img.shields.io/pypi/dm/pytest-schema.svg)](https://pypi.python.org/pypi/pytest-schema/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


👍 Validate return values against a schema-like object in testing

[`keleshev/schema`](https://github.com/keleshev/schema) is a library for validating Python data structures, such as
those obtained from config-files, forms, external services or
command-line parsing, converted from JSON/YAML (or something else) to Python data-types.

## Install

```bash
pip install pytest-schema
```

## Basic Example

Here is a quick example of using **`schema`**:
```python
from pytest_schema import schema, exact_schema, like_schema

article_v1 = {
    "id": int,
    "title": str,
    "completed": bool,
    "engagement": {
        "viewer": list,
        "rating": float,
    },
    "metadata": dict
}

def test_article_v1_endpoint(test_client):
    """
    Test calling v1 endpoint and validating the response
    is in the correctly/expected format.
    """
    response_v1 = test_client.get("/api/v1/article/1")
    assert exact_schema(article_v1) == response_v1
    # Same as:
    # assert schema(article_v1) == response_v1

article_v2 = {
    **article_v1,
    "someNewField": int
}

def test_article_v2_endpoint(test_client):
    """
    Test calling v2 endpoint is backwards compatible with v1
    """
    response_v2 = test_client.get("/api/v2/article/1")

    assert like_schema(article_v1) == response_v2

```
## Full Example

Here is a more complex example of using **`schema`**:

``` python
import pytest
from pytest_schema import schema, And, Enum, Optional, Or, Regex, SchemaError

# single user schema
user = {
    # id must be int
    "id": int,
    # name must be type str
    "name": str,
    # description must be type str or nullable
    "description": Or(None, str),
    # email valid str format
    "email": Regex(r".*?@.*?\.[A-Za-z]{2,6}"),
    # age converted to int then validated gt 18 lt 99 and must be type str
    "age": And(int, lambda n: 18 <= n <= 99),
    # gender key is optional but must be str
    Optional("gender"): str,
    # role of enum values
    "role": Enum("user", "super-user", "admin"),
    # list of ids ref friends
    "friends": [ int ],
    # nested dict to valid as address
    "address": {
        "street": str,
        Optional("street2"): str,
        "city": str,
        "state": And(str, lambda s: len(s) == 2),
        "zipcode": str,
    }

}

# multiple users schema
users = [ user ]

def test_users_endpoint():
    """
    Test calling a users endpoint and validating its
    response of users info is correct format.
    """
    response = [
        # ✅ Valid 
        {
            "id": 2,
            "name": "Sue",
            "description": "Sue, the admin",
            "age": 28,
            "email": "sue@gmail.com",
            "gender": "female",
            "role": "admin",
            "friends": [5, 6],
            "address": {
                "street": "123 Washington Ave.",
                "city": "New York",
                "state": "NY",
                "zipcode": "099012",
            }
        },
        # ✅ Valid
        {
            "id": 5,
            "name": "Sam",
            "description": "Sam, the user",
            "age": 42,
            "email": "sam@aol.com",
            "role": "user",
            "friends": [2, 6, 7],
            "address": {
                "street": "5 Sunset St.",
                "street2": "Apt # 55-b",
                "city": "San Jose",
                "state": "CA",
                "zipcode": "054053",
            }
        },
    ]

    assert schema(users) == response

def test_users_endpoint_INVALID():
    """
    Test calling a users endpoint and validating its
    response of users info is INVALID format.
    """
    response = [
        # ❌ Invalid
        {
            "id": "null",
            "name": None,
            "age": 0,
            "email": "unknown@msn",
            "role": "unknown",
            "friends": None,
            "address": "5 Sunset St., San Jose, CA, 054053",
        },
    ]

    # Option 1:
    assert schema(users) != response
    
    # Option 2:
    with pytest.raises(SchemaError):
        schema(users) == response

```

If data is **`valid`**, it will return the `True`.
If data is **`invalid`**, it will raise `SchemaError` exception.


## Supported validations

See: [keleshev/schema](https://github.com/keleshev/schema) full documentation.
