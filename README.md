# pytest-schema
👍 Validate return values against a schema-like object in testing

[schema v0.7](https://github.com/keleshev/schema) is a library for validating Python data structures, such as
those obtained from config-files, forms, external services or
command-line parsing, converted from JSON/YAML (or something else) to Python data-types.

## Example

Here is a quick example to get a feeling of **schema**, validating a
list of entries with personal information:

``` python
from pytest_schema import schema, And, Enum, Optional, Or, Regex

# single user schema
user = {
    # id must be int
    "id": int,
    # name must be type str
    "name": str,
    # email must be type str or nullable
    "description": Or(None, str),
    # email valid str format
    "email": Regex(r".*?@.*?\.[A-Za-z]{2,6}"),
    # age converted to int then validated gt 18 lt 99 and must be type str
    "age": And(int, lambda n: 18 <= n <= 99),
    # gender key is optional but must be str
    Optional("gender"): str,
    # role of enum values
    "role": Enum(["user", "super-user", "admin"]),
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
    Test calling a users endpoint and its response of users info.
    """
    response = [
        # ✅ Valid 
        {
            "id": 2,
            "name": "Sue",
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
            "id": 5
            "name": "Sam",
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

    assert schema(users) == response

```

If data is **`valid`**, it will return the `True`.
If data is **`invalid`**, it will raise `SchemaError` exception.

## Installation

Use [`pip`](http://pip-installer.org):
```bash
pip install pytest-schema
```

## Supported validations

The resulting JSON schema is not guaranteed to accept the same objects
as the library would accept, since some validations are not implemented
or have no JSON schema equivalent. This is the case of the `Use` and
`Hook` objects for example.

### [Object properties](https://json-schema.org/understanding-json-schema/reference/object.html#properties)  

Use a dict literal. The dict keys are the JSON schema properties.
    
Python:
```python
{ "test": str }
```

Json Schema:
```json
{
    "type": "object",
    "properties": {
        "test": {"type": "string"}
    },
    "required": ["test"],
    "additionalProperties": false,
}
```

Please note that attributes are required by default. To create
optional attributes use `Optional`, like so:

Python:

```python
{ Optional("test"): str }
```
    
Json Schema:
```json
{
    "type": "object", 
    "properties": {
        "test": { "type": "string" }
    },
    "required": [],
    "additionalProperties": false
}
```

### Types  

Use the Python type name directly. It will be converted to the JSON name:

| Python | Json | Json Schema|
| - | - | - |
| `str` | [string](https://json-schema.org/understanding-json-schema/reference/string.html)| `{ "type": "string" }` |
|`int` | [integer](https://json-schema.org/understanding-json-schema/reference/numeric.html#integer) | `{ "type": "integer" }`  |
| `float` | [number](https://json-schema.org/understanding-json-schema/reference/numeric.html#number) | `{ "type": "number" }` |
| `bool` | [boolean](https://json-schema.org/understanding-json-schema/reference/boolean.html) | `{ "type": "boolean" }` |
| `list` | [array](https://json-schema.org/understanding-json-schema/reference/array.html) | `{ "type": "array" }` |
| `dict` | [object](https://json-schema.org/understanding-json-schema/reference/object.html) | `{ "type": "object" }`  |

### [Array items](https://json-schema.org/understanding-json-schema/reference/array.html#items)  

Surround a schema with `[]`.
    
Python:
```python
[str] # means an array of string and becomes
```

Json Schema:
```json
{
    "type": "array",
    "items": { "type": "string" }
}
```

### [Enumerated values](https://json-schema.org/understanding-json-schema/reference/generic.html#enumerated-values)  

Use `Enum` or `Or`.

Python:
```python
Enum([1, 2, 3])
# or
Or(1, 2, 3)
```
 
Json Schema: 
```json
{ "enum": [1, 2, 3] }
```

### [Constant values](https://json-schema.org/understanding-json-schema/reference/generic.html#constant-values)  

Use the value itself or `Const`.
    
Python:
```python
"name"
# or
Const("name")
```

```json
{ "const": "name" }
```

### [Regular expressions](https://json-schema.org/understanding-json-schema/reference/regular_expressions.html)  
Use `Regex`.
    
Python:
```python
Regex(r"^v\d+")
```

Json Schema:
```json
{
    "type": "string",
    "pattern": "^v\\d+"
}
```

### [Combining schemas with allOf](https://json-schema.org/understanding-json-schema/reference/combining.html#allof)  

Use `And`.
    
Python:
```python
And(str, "value")
```

Json Schema:
```json
{
    "allOf": [
        { "type": "string" },
        { "const": "value" }
    ]
}
```

_Note that this example is not really useful in the real world, since
`const` already implies the type._

### [Combining schemas with anyOf](https://json-schema.org/understanding-json-schema/reference/combining.html#anyof)  

Use `Or`.
    
Python:
```python
Or(str, int)
```

Json Schema:
```json
{
    "anyOf": [
        { "type": "string" },
        { "type": "integer" }
    ]
}
```