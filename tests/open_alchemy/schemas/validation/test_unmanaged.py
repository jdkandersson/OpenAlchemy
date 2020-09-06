"""Tests for unmanaged validation."""

import pytest

from open_alchemy.schemas import validation

CHECK_MODEL_TESTS = [
    pytest.param(
        {},
        {},
        {
            "result": {
                "valid": False,
                "reason": 'no "type" key was found, define a type',
            }
        },
        id="empty",
    ),
    pytest.param(
        {"type": True},
        {},
        {
            "result": {
                "valid": False,
                "reason": "the type value is True, change it to a string value",
            }
        },
        id="type value not string",
    ),
    pytest.param(
        {"type": "not object"},
        {},
        {
            "result": {
                "valid": False,
                "reason": (
                    'the type of the schema is "not object", change it to be "object"'
                ),
            }
        },
        id="type not object",
    ),
    pytest.param(
        {"$ref": True},
        {},
        {
            "result": {
                "valid": False,
                "reason": "malformed schema :: The value of $ref must be a string. ",
            }
        },
        id="$ref not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        {
            "result": {
                "valid": False,
                "reason": "reference :: 'RefSchema was not found in schemas.' ",
            }
        },
        id="$ref unresolved",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "not object"}},
        {
            "result": {
                "valid": False,
                "reason": (
                    'the type of the schema is "not object", change it to be "object"'
                ),
            }
        },
        id="$ref type not object",
    ),
    pytest.param(
        {"allOf": True},
        {},
        {
            "result": {
                "valid": False,
                "reason": "malformed schema :: The value of allOf must be a list. ",
            }
        },
        id="allOf not list",
    ),
    pytest.param(
        {"allOf": [{"type": "not object"}]},
        {},
        {
            "result": {
                "valid": False,
                "reason": (
                    'the type of the schema is "not object", change it to be "object"'
                ),
            }
        },
        id="allOf not object",
    ),
    pytest.param(
        {"type": "object"},
        {},
        {
            "result": {
                "valid": False,
                "reason": (
                    'no "x-tablename" key was found, define the name of the table'
                ),
            }
        },
        id="tablename not present",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        {
            "result": {
                "valid": False,
                "reason": (
                    'no "x-tablename" key was found, define the name of the table'
                ),
            }
        },
        id="$ref tablename not present",
    ),
    pytest.param(
        {"allOf": [{"type": "object"}]},
        {},
        {
            "result": {
                "valid": False,
                "reason": (
                    'no "x-tablename" key was found, define the name of the table'
                ),
            }
        },
        id="allOf tablename not present",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", CHECK_MODEL_TESTS)
@pytest.mark.schemas
def test_check_model(schema, schemas, expected_result):
    """
    GIVEN schema and schemas and the expected result
    WHEN check_model is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = validation.unmanaged.check_model(schemas, schema)

    assert returned_result == expected_result


CHECK_MODELS_TESTS = [
    pytest.param({}, {}, id="empty"),
    pytest.param({"Schema1": {"x-tablename": True}}, {}, id="single constructable"),
    pytest.param(
        {"Schema1": {}},
        {
            "Schema1": {
                "result": {
                    "valid": False,
                    "reason": 'no "type" key was found, define a type',
                }
            }
        },
        id="single not constructable",
    ),
    pytest.param(
        {"Schema1": {"x-tablename": True}, "Schema2": {"x-tablename": True}},
        {},
        id="multiple all constructable",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": {"x-tablename": True}},
        {
            "Schema1": {
                "result": {
                    "valid": False,
                    "reason": 'no "type" key was found, define a type',
                }
            }
        },
        id="multiple first not constructable",
    ),
    pytest.param(
        {"Schema1": {"x-tablename": True}, "Schema2": {}},
        {
            "Schema2": {
                "result": {
                    "valid": False,
                    "reason": 'no "type" key was found, define a type',
                }
            }
        },
        id="multiple second not constructable",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": {"type": "object"}},
        {
            "Schema1": {
                "result": {
                    "valid": False,
                    "reason": 'no "type" key was found, define a type',
                }
            },
            "Schema2": {
                "result": {
                    "valid": False,
                    "reason": (
                        'no "x-tablename" key was found, define the name of the table'
                    ),
                }
            },
        },
        id="multiple all not constructable",
    ),
]


@pytest.mark.parametrize("schemas, expected_result", CHECK_MODELS_TESTS)
@pytest.mark.schemas
def test_check_models(schemas, expected_result):
    """
    GIVEN schemas and the expected result
    WHEN check_models is called with the schemas
    THEN the expected result is returned.
    """
    returned_result = validation.unmanaged.check_models(schemas=schemas)

    assert returned_result == expected_result


CHECK_TESTS = [
    pytest.param(
        True,
        {"result": {"valid": False, "reason": "specification must be a dictionary"}},
        id="spec not dict",
    ),
    pytest.param(
        {"components": {"schemas": {}}},
        {"result": {"valid": True}, "models": {}},
        id="schemas empty",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {}}}},
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {
                        "valid": False,
                        "reason": 'no "type" key was found, define a type',
                    }
                }
            },
        },
        id="single model model not constructable",
    ),
]


@pytest.mark.parametrize("spec, expected_result", CHECK_TESTS)
@pytest.mark.schemas
def test_check(spec, expected_result):
    """
    GIVEN spec and the expected result
    WHEN check is called with the spec
    THEN the expected result is returned.
    """
    returned_result = validation.unmanaged.check(spec=spec)

    assert returned_result == expected_result
