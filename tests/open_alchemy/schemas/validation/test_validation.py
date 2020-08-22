"""Tests for validation rules."""

import pytest

from open_alchemy import exceptions
from open_alchemy.schemas import validation

PROCESS_TESTS = [
    pytest.param(True, True, id="not dictionary"),
    pytest.param({}, True, id="empty"),
    pytest.param({"Schema1": {}}, True, id="model not constructable"),
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
                    },
                    "properties": {},
                }
            },
        },
        id="single model model not valid no properties",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {"Schema1": {"x-tablename": "schema_1", "properties": True}}
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
                    },
                    "properties": {},
                }
            },
        },
        id="single model model not valid properties not dict",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "x-tablename": "schema_1",
                        "properties": {True: {"type": "integer"}},
                    }
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
                    },
                    "properties": {},
                }
            },
        },
        id="single model model not valid properties key not string",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": True},
                    }
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
                    },
                    "properties": {
                        "prop_1": {
                            "result": {
                                "valid": False,
                                "reason": (
                                    "malformed schema :: The schema must be a "
                                    "dictionary. "
                                ),
                            }
                        }
                    },
                }
            },
        },
        id="single model model not valid properties value not dict",
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
                    },
                    "properties": {},
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
                    },
                    "properties": {},
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
