"""Tests for artifacts."""

import pytest

from open_alchemy.schemas import artifacts

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
