"""Tests for validation rules."""

import pytest

from open_alchemy import exceptions
from open_alchemy.schemas import validation

PROCESS_TESTS = [
    pytest.param(True, True, id="not dictionary"),
    pytest.param({}, True, id="empty"),
    pytest.param({True: {}}, True, id="key not string"),
    pytest.param({"Schema1": True}, True, id="value not dict"),
    pytest.param({"Schema1": {}}, True, id="model not constructable"),
    pytest.param(
        {True: {}, "Schema2": {}}, True, id="multiple model first key not string"
    ),
    pytest.param(
        {"Schema1": {}, True: {}}, True, id="multiple model second key not string"
    ),
    pytest.param(
        {"Schema1": True, "Schema2": {}}, True, id="multiple model first value not dict"
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": True},
        True,
        id="multiple model second value not dict",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": {}}, True, id="multiple model not constructable"
    ),
    pytest.param({"Schema1": {"x-tablename": "schema_1"}}, True, id="model not valid"),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {}},
            }
        },
        True,
        id="model property not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        False,
        id="model valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {}, "prop_2": {"type": "integer"}},
            }
        },
        True,
        id="model multiple properties first property not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}, "prop_2": {}},
            }
        },
        True,
        id="model multiple properties second property not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {"type": "integer"},
                    "prop_2": {"type": "integer"},
                },
            }
        },
        False,
        id="model multiple properties valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {}},
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        True,
        id="multiple model first not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_2": {}},
            },
        },
        True,
        id="multiple model second not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        False,
        id="multiple model valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {
                        "properties": {
                            "column": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    }
                ]
            },
        },
        False,
        id="model allOf",
    ),
]


@pytest.mark.parametrize("schemas, raises", PROCESS_TESTS)
@pytest.mark.schemas
def test_process(schemas, raises):
    """
    GIVEN schemas and whether an exception is expected
    WHEN process is called with the schemas
    THEN MalformedSchemaError is raised is raises is set otherwise it is not.
    """
    if raises:
        with pytest.raises(exceptions.MalformedSchemaError):
            validation.process(schemas=schemas)
    else:
        validation.process(schemas=schemas)


CHECK_TESTS = [
    pytest.param(
        True,
        {"result": {"valid": False, "reason": "specification must be a dictionary"}},
        id="spec not dict",
    ),
    pytest.param(
        {},
        {"result": {"valid": False, "reason": "specification must define components"}},
        id="no components key",
    ),
    pytest.param(
        {"components": True},
        {"result": {"valid": False, "reason": "components value must be a dictionary"}},
        id="components value not dict",
    ),
    pytest.param(
        {"components": {}},
        {"result": {"valid": False, "reason": "specification must define schemas"}},
        id="no schemas",
    ),
    pytest.param(
        {"components": {"schemas": True}},
        {"result": {"valid": False, "reason": "schemas must be a dictionary"}},
        id="schemas not dict",
    ),
    pytest.param(
        {"components": {"schemas": {}}},
        {
            "result": {
                "valid": False,
                "reason": "specification must define at least 1 schema with the "
                "x-tablename key",
            }
        },
        id="schemas empty",
    ),
    pytest.param(
        {"components": {"schemas": {True: {}}}},
        {
            "result": {
                "valid": False,
                "reason": "schemas keys must be strings, True is not",
            }
        },
        id="schemas key not string",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": True}}},
        {
            "result": {
                "valid": False,
                "reason": "the value of Schema1 must be a dictionary",
            }
        },
        id="schemas values not dict",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {}}}},
        {
            "result": {
                "valid": False,
                "reason": "specification must define at least 1 schema with the "
                "x-tablename key",
            }
        },
        id="single model model not constructable",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {"x-tablename": "schema_1"}}}},
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {
                        "valid": False,
                        "reason": "malformed schema :: Every property requires a "
                        "type. ",
                    }
                }
            },
        },
        id="single model model not valid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {}},
                    }
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {
                        "prop_1": {
                            "result": {
                                "valid": False,
                                "reason": "malformed schema :: Every property requires "
                                "a type. ",
                            }
                        }
                    },
                }
            },
        },
        id="single model properties not valid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                    }
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {"prop_1": {"result": {"valid": True}}},
                }
            },
        },
        id="single model valid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {}, "prop_2": {"type": "integer"}},
                    }
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {
                        "prop_1": {
                            "result": {
                                "valid": False,
                                "reason": "malformed schema :: Every property requires "
                                "a type. ",
                            }
                        },
                        "prop_2": {"result": {"valid": True}},
                    },
                }
            },
        },
        id="single model multiple properties first invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}, "prop_2": {}},
                    }
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {
                        "prop_1": {"result": {"valid": True}},
                        "prop_2": {
                            "result": {
                                "valid": False,
                                "reason": "malformed schema :: Every property requires "
                                "a type. ",
                            }
                        },
                    },
                }
            },
        },
        id="single model multiple properties second invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {
                            "prop_1": {"type": "integer"},
                            "prop_2": {"type": "integer"},
                        },
                    }
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {
                        "prop_1": {"result": {"valid": True}},
                        "prop_2": {"result": {"valid": True}},
                    },
                }
            },
        },
        id="single model multiple properties valid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    True: {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                    "Schema2": {
                        "type": "object",
                        "x-tablename": "schema_2",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                }
            }
        },
        {
            "result": {
                "valid": False,
                "reason": "schemas keys must be strings, True is not",
            }
        },
        id="multiple model first key invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                    True: {
                        "type": "object",
                        "x-tablename": "schema_2",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                }
            }
        },
        {
            "result": {
                "valid": False,
                "reason": "schemas keys must be strings, True is not",
            }
        },
        id="multiple model second key invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": True,
                    "Schema2": {
                        "type": "object",
                        "x-tablename": "schema_2",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                }
            }
        },
        {
            "result": {
                "valid": False,
                "reason": "the value of Schema1 must be a dictionary",
            }
        },
        id="multiple model first value invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                    "Schema2": True,
                }
            }
        },
        {
            "result": {
                "valid": False,
                "reason": "the value of Schema2 must be a dictionary",
            }
        },
        id="multiple model second value invalid",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {}, "Schema2": {}}}},
        {
            "result": {
                "valid": False,
                "reason": "specification must define at least 1 schema with the "
                "x-tablename key",
            }
        },
        id="multiple model not constructable",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {"x-tablename": "schema_1"},
                    "Schema2": {
                        "type": "object",
                        "x-tablename": "schema_2",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {
                        "valid": False,
                        "reason": "malformed schema :: Every property requires a "
                        "type. ",
                    }
                },
                "Schema2": {
                    "result": {"valid": True},
                    "properties": {"prop_1": {"result": {"valid": True}}},
                },
            },
        },
        id="multiple model first model invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                    "Schema2": {"x-tablename": "schema_2"},
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {"prop_1": {"result": {"valid": True}}},
                },
                "Schema2": {
                    "result": {
                        "valid": False,
                        "reason": "malformed schema :: Every property requires a "
                        "type. ",
                    }
                },
            },
        },
        id="multiple model second model invalid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                    "Schema2": {
                        "type": "object",
                        "x-tablename": "schema_2",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                }
            }
        },
        {
            "result": {"valid": True},
            "models": {
                "Schema1": {
                    "result": {"valid": True},
                    "properties": {"prop_1": {"result": {"valid": True}}},
                },
                "Schema2": {
                    "result": {"valid": True},
                    "properties": {"prop_1": {"result": {"valid": True}}},
                },
            },
        },
        id="multiple model valid",
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
    returned_result = validation.check(spec=spec)

    assert returned_result == expected_result
