"""Integration tests for from_dict and to_dict."""

from unittest import mock

import pytest

import open_alchemy


@pytest.mark.integration
def test_to_from_dict():
    """
    GIVEN specification that has schema with a single property
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "Table": {
                        "properties": {"column": {"type": "integer"}},
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
    )
    model = model_factory(name="Table")

    # COnstructing and turning back to dictionary
    model_dict = {"column": 1}
    instance = model.from_dict(**model_dict)
    assert instance.to_dict() == model_dict


@pytest.mark.integration
def test_to_from_dict_relationship():
    """
    GIVEN specification that has a schema with a relationship
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {"id": {"type": "integer"}},
                        "x-tablename": "table",
                        "type": "object",
                    },
                    "Table": {
                        "properties": {
                            "column": {"$ref": "#/components/schemas/RefTable"}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
    )
    model_factory(name="RefTable")
    model = model_factory(name="Table")

    # COnstructing and turning back to dictionary
    model_dict = {"column": {"id": 1}}
    instance = model.from_dict(**model_dict)
    assert instance.to_dict() == model_dict
