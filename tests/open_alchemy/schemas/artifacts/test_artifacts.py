"""Tests for artifacts."""

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas import helpers

GET_TESTS = [
    pytest.param(
        True,
        {},
        id="spec not dict",
    ),
    pytest.param(
        {"components": {"schemas": {}}},
        {"models": {}},
        id="schemas empty",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {}}}},
        {"models": {}},
        id="single model model not constructable",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {"x-tablename": "schema_1"}}}},
        {"models": {}},
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
            "models": {
                "Schema1": {"artifacts": {"tablename": "schema_1"}, "properties": {}}
            }
        },
        id="single model single property invalid",
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
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        }
                    },
                }
            }
        },
        id="single model single property valid not required",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {"type": "integer"}},
                        "required": ["prop_1"],
                    }
                }
            }
        },
        {
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": True,
                            }
                        }
                    },
                }
            }
        },
        id="single model single property valid required",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {}, "prop_2": {}},
                    }
                }
            }
        },
        {
            "models": {
                "Schema1": {"artifacts": {"tablename": "schema_1"}, "properties": {}}
            }
        },
        id="single model multiple property none valid",
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
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        }
                    },
                }
            }
        },
        id="single model multiple property first valid",
    ),
    pytest.param(
        {
            "components": {
                "schemas": {
                    "Schema1": {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"prop_1": {}, "prop_2": {"type": "string"}},
                    }
                }
            }
        },
        {
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_2": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "string"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "string"},
                                "required": False,
                            }
                        }
                    },
                }
            }
        },
        id="single model multiple property second valid",
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
                            "prop_2": {"type": "string"},
                        },
                    }
                }
            }
        },
        {
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        },
                        "prop_2": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "string"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "string"},
                                "required": False,
                            }
                        },
                    },
                }
            }
        },
        id="single model multiple property valid",
    ),
    pytest.param(
        {"components": {"schemas": {"Schema1": {}, "Schema2": {}}}},
        {"models": {}},
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
            "models": {
                "Schema2": {
                    "artifacts": {"tablename": "schema_2"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        }
                    },
                }
            }
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
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        }
                    },
                }
            }
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
            "models": {
                "Schema1": {
                    "artifacts": {"tablename": "schema_1"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        }
                    },
                },
                "Schema2": {
                    "artifacts": {"tablename": "schema_2"},
                    "properties": {
                        "prop_1": {
                            "artifacts": {
                                "type": "SIMPLE",
                                "open_api": {"type": "integer"},
                                "extension": {"primary_key": False},
                                "schema": {"type": "integer"},
                                "required": False,
                            }
                        }
                    },
                },
            },
        },
        id="multiple model valid",
    ),
]


def _construct_model_artifacts(tablename, inherits, parent, properties):
    """Construct model artifacts"""
    return artifacts.types.ModelArtifacts(
        tablename=tablename,
        inherits=inherits,
        parent=parent,
        description=None,
        mixins=None,
        kwargs=None,
        composite_index=None,
        composite_unique=None,
        backrefs=[],
        properties=properties,
    )


def _construct_simple_property_artifacts(type_, required):
    """Construct the artifacts for a simple property."""
    return artifacts.types.SimplePropertyArtifacts(
        type=helpers.property_.type_.Type.SIMPLE,
        open_api=artifacts.types.OpenApiSimplePropertyArtifacts(
            type=type_,
            format=None,
            max_length=None,
            nullable=None,
            default=None,
            read_only=None,
            write_only=None,
        ),
        extension=artifacts.types.ExtensionSimplePropertyArtifacts(
            primary_key=False,
            autoincrement=None,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=None,
        ),
        schema={"type": type_},
        required=required,
        description=None,
    )


@pytest.mark.parametrize("spec, expected_artifacts", GET_TESTS)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_get(spec, expected_artifacts):
    """
    GIVEN spec and the expected artifacts
    WHEN get is called with the spec
    THEN the expected artifacts is returned.
    """
    returned_artifacts = artifacts.get(spec=spec)

    assert returned_artifacts == expected_artifacts


GET_FROM_SCHEMAS_TESTS = [
    pytest.param(
        {},
        False,
        [],
        id="no model",
    ),
    pytest.param(
        {"Schema1": {}},
        False,
        [],
        id="single model not constructable",
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
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "schema_1",
                    None,
                    None,
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        )
                    ],
                ),
            )
        ],
        id="single model single property not required",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
                "required": ["prop_1"],
            }
        },
        False,
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "schema_1",
                    None,
                    None,
                    [("prop_1", _construct_simple_property_artifacts("integer", True))],
                ),
            )
        ],
        id="single model single property required",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {"$ref": "#/components/schemas/ParentSchema"},
                    {
                        "x-inherits": True,
                        "type": "object",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                ]
            },
            "ParentSchema": {
                "type": "object",
                "x-tablename": "parent",
                "properties": {"prop_2": {"type": "string"}},
            },
        },
        False,
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "parent",
                    True,
                    "ParentSchema",
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        ),
                        (
                            "prop_2",
                            _construct_simple_property_artifacts("string", False),
                        ),
                    ],
                ),
            ),
            (
                "ParentSchema",
                _construct_model_artifacts(
                    "parent",
                    None,
                    None,
                    [("prop_2", _construct_simple_property_artifacts("string", False))],
                ),
            ),
        ],
        id="single model inherits property on parent stay within model False",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {"$ref": "#/components/schemas/ParentSchema"},
                    {
                        "x-inherits": True,
                        "type": "object",
                        "properties": {"prop_1": {"type": "integer"}},
                    },
                ]
            },
            "ParentSchema": {
                "type": "object",
                "x-tablename": "parent",
                "properties": {"prop_2": {"type": "string"}},
            },
        },
        True,
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "parent",
                    True,
                    "ParentSchema",
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        )
                    ],
                ),
            ),
            (
                "ParentSchema",
                _construct_model_artifacts(
                    "parent",
                    None,
                    None,
                    [("prop_2", _construct_simple_property_artifacts("string", False))],
                ),
            ),
        ],
        id="single model inherits property on parent stay within model True",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {"type": "integer"},
                    "prop_2": {"type": "string"},
                },
            }
        },
        False,
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "schema_1",
                    None,
                    None,
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        ),
                        (
                            "prop_2",
                            _construct_simple_property_artifacts("string", False),
                        ),
                    ],
                ),
            )
        ],
        id="single model multiple property valid",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": {}},
        False,
        [],
        id="multiple model none constructable",
    ),
    pytest.param(
        {
            "Schema1": {},
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_1": {"type": "integer"}},
            },
        },
        False,
        [
            (
                "Schema2",
                _construct_model_artifacts(
                    "schema_2",
                    None,
                    None,
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        )
                    ],
                ),
            )
        ],
        id="multiple first not constructable",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {},
        },
        False,
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "schema_1",
                    None,
                    None,
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        )
                    ],
                ),
            )
        ],
        id="multiple second not constructable",
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
                "properties": {"prop_1": {"type": "integer"}},
            },
        },
        False,
        [
            (
                "Schema1",
                _construct_model_artifacts(
                    "schema_1",
                    None,
                    None,
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        )
                    ],
                ),
            ),
            (
                "Schema2",
                _construct_model_artifacts(
                    "schema_2",
                    None,
                    None,
                    [
                        (
                            "prop_1",
                            _construct_simple_property_artifacts("integer", False),
                        )
                    ],
                ),
            ),
        ],
        id="multiple all constructable",
    ),
]


@pytest.mark.parametrize(
    "schemas, stay_within_model, expected_artifacts", GET_FROM_SCHEMAS_TESTS
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_get_from_schemas(schemas, stay_within_model, expected_artifacts):
    """
    GIVEN schemas and the expected artifacts
    WHEN get_from_schemas is called with the schemas
    THEN the expected artifacts is returned.
    """
    returned_artifacts = artifacts.get_from_schemas(
        schemas=schemas, stay_within_model=stay_within_model
    )

    assert returned_artifacts == expected_artifacts
