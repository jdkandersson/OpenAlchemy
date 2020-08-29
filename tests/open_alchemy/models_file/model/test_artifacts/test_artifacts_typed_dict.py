"""Tests for artifacts."""
# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file

_ColSchemaArtifacts = models_file.types.ColumnSchemaArtifacts
_ColSchemaOAArtifacts = models_file.types.ColumnSchemaOpenAPIArtifacts
_ColSchemaExtArtifacts = models_file.types.ColumnSchemaExtensionArtifacts
_ColumnArtifacts = models_file.types.ColumnArtifacts
_ColumnArgArtifacts = models_file.types.ColumnArgArtifacts


@pytest.mark.parametrize(
    "schema, expected_props",
    [
        pytest.param(
            {"properties": {}},
            [],
            id="empty",
        ),
        pytest.param(
            {"properties": {"column_1": {"type": "integer"}}},
            [],
            id="single required not given",
        ),
        pytest.param(
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [],
            id="single not required",
        ),
        pytest.param(
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [_ColumnArtifacts(name="column_1", type="int")],
            id="single required",
        ),
        pytest.param(
            {
                "properties": {"column_1": {"type": "integer", "writeOnly": True}},
                "required": ["column_1"],
            },
            [],
            id="single required writeOnly True",
        ),
        pytest.param(
            {
                "properties": {"column_1": {"type": "integer", "writeOnly": False}},
                "required": ["column_1"],
            },
            [_ColumnArtifacts(name="column_1", type="int")],
            id="single required writeOnly False",
        ),
        pytest.param(
            {
                "properties": {"column_1": {"type": "object", "x-de-$ref": "RefModel"}},
                "required": ["column_1"],
            },
            [_ColumnArtifacts(name="column_1", type='"RefModelDict"')],
            id="single required object",
        ),
        pytest.param(
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                },
                "required": ["column_1", "column_2"],
            },
            [
                _ColumnArtifacts(name="column_1", type="int"),
                _ColumnArtifacts(name="column_2", type="str"),
            ],
            id="multiple required",
        ),
        pytest.param(
            {
                "properties": {
                    "column_1": {"type": "integer", "writeOnly": True},
                    "column_2": {"type": "string"},
                },
                "required": ["column_1", "column_2"],
            },
            [_ColumnArtifacts(name="column_2", type="str")],
            id="multiple required first writeOnly",
        ),
        pytest.param(
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string", "writeOnly": True},
                },
                "required": ["column_1", "column_2"],
            },
            [_ColumnArtifacts(name="column_1", type="int")],
            id="multiple required second writeOnly",
        ),
        pytest.param(
            {
                "properties": {
                    "column_1": {"type": "integer", "writeOnly": True},
                    "column_2": {"type": "string", "writeOnly": True},
                },
                "required": ["column_1", "column_2"],
            },
            [],
            id="multiple required all writeOnly",
        ),
    ],
)
@pytest.mark.models_file
def test_calculate_td_required_props(schema, expected_props):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td required properties are added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    # assert False
    assert artifacts.typed_dict.required.props == expected_props


@pytest.mark.parametrize(
    "schema, expected_props",
    [
        pytest.param(
            {"properties": {}},
            [],
            id="empty",
        ),
        pytest.param(
            {"properties": {"column_1": {"type": "integer"}}},
            [_ColumnArtifacts(name="column_1", type="typing.Optional[int]")],
            id="single required not given",
        ),
        pytest.param(
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [_ColumnArtifacts(name="column_1", type="typing.Optional[int]")],
            id="single not required",
        ),
        pytest.param(
            {
                "properties": {"column_1": {"type": "integer", "writeOnly": True}},
                "required": [],
            },
            [],
            id="single not required writeOnly",
        ),
        pytest.param(
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [],
            id="single required",
        ),
        pytest.param(
            {
                "properties": {"column_1": {"type": "object", "x-de-$ref": "RefModel"}},
                "required": [],
            },
            [_ColumnArtifacts(name="column_1", type='typing.Optional["RefModelDict"]')],
            id="single not required object",
        ),
        pytest.param(
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                },
                "required": [],
            },
            [
                _ColumnArtifacts(name="column_1", type="typing.Optional[int]"),
                _ColumnArtifacts(name="column_2", type="typing.Optional[str]"),
            ],
            id="multiple not required",
        ),
    ],
)
@pytest.mark.models_file
def test_calculate_td_not_required_props(schema, expected_props):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td not required properties are added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.typed_dict.not_required.props == expected_props


@pytest.mark.parametrize(
    "schema, expected_required_empty",
    [
        ({"properties": {}}, True),
        ({"properties": {"column_1": {"type": "integer"}}}, True),
        ({"properties": {"column_1": {"type": "integer"}}, "required": []}, True),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            False,
        ),
    ],
    ids=[
        "empty",
        "single required not given",
        "single not required",
        "single required",
    ],
)
@pytest.mark.models_file
def test_calculate_required_empty(schema, expected_required_empty):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td required empty is added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.typed_dict.required.empty == expected_required_empty


@pytest.mark.parametrize(
    "schema, expected_not_required_empty",
    [
        ({"properties": {}}, True),
        ({"properties": {"column_1": {"type": "integer"}}}, False),
        ({"properties": {"column_1": {"type": "integer"}}, "required": []}, False),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            True,
        ),
    ],
    ids=[
        "empty",
        "single required not given",
        "single not required",
        "single required",
    ],
)
@pytest.mark.models_file
def test_calculate_not_required_empty(schema, expected_not_required_empty):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td not required empty is added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.typed_dict.not_required.empty == expected_not_required_empty


# Table for the name of the required and not required TypedDicts
# +----------------+--------------------+-----------------------+-------------------+
# | required empty | not required empty | required name         | not required name |
# +================+====================+=======================+===================+
# | False          | False              | _<model name>DictBase | <model name>Dict  |
# +----------------+--------------------+-----------------------+-------------------+
# | False          | True               | <model name>Dict      | None              |
# +----------------+--------------------+-----------------------+-------------------+
# | True           | False              | None                  | <model name>Dict  |
# +----------------+--------------------+-----------------------+-------------------+
# | True           | True               | None                  | <model name>Dict  |
# +----------------+--------------------+-----------------------+-------------------+


@pytest.mark.parametrize(
    "schema, expected_required_name, expected_not_required_name",
    [
        (
            {
                "properties": {
                    "column_1": {"type": "string"},
                    "column_2": {"type": "string"},
                },
                "required": ["column_1"],
            },
            "_ModelDictBase",
            "ModelDict",
        ),
        (
            {"properties": {"column_1": {"type": "string"}}, "required": ["column_1"]},
            "ModelDict",
            None,
        ),
        (
            {"properties": {"column_1": {"type": "string"}}, "required": []},
            None,
            "ModelDict",
        ),
        ({"properties": {}}, None, "ModelDict"),
    ],
    ids=[
        "required empty: False, not required empty: False",
        "required empty: False, not required empty: True",
        "required empty: True,  not required empty: False",
        "required empty: True,  not required empty: True",
    ],
)
@pytest.mark.models_file
def test_calculate_td_names(schema, expected_required_name, expected_not_required_name):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td required and not required names are added to the
        artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.typed_dict.required.name == expected_required_name
    assert artifacts.typed_dict.not_required.name == expected_not_required_name


# Table for the parent class of the required and not required TypedDicts
# +----------------+--------------------+------------------+-----------------------+
# | required empty | not required empty | required parent  | not required parent   |
# +================+====================+==================+=======================+
# | False          | False              | typing.TypedDict | _<model name>DictBase |
# +----------------+--------------------+------------------+-----------------------+
# | False          | True               | typing.TypedDict | None                  |
# +----------------+--------------------+------------------+-----------------------+
# | True           | False              | None             | typing.TypedDict      |
# +----------------+--------------------+------------------+-----------------------+
# | True           | True               | None             | typing.TypedDict      |
# +----------------+--------------------+------------------+-----------------------+


_EXPECTED_TD_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_TD_BASE = "typing_extensions.TypedDict"


@pytest.mark.parametrize(
    "schema, expected_required_parent, expected_not_required_parent",
    [
        (
            {
                "properties": {
                    "column_1": {"type": "string"},
                    "column_2": {"type": "string"},
                },
                "required": ["column_1"],
            },
            _EXPECTED_TD_BASE,
            "_ModelDictBase",
        ),
        (
            {"properties": {"column_1": {"type": "string"}}, "required": ["column_1"]},
            _EXPECTED_TD_BASE,
            None,
        ),
        (
            {"properties": {"column_1": {"type": "string"}}, "required": []},
            None,
            _EXPECTED_TD_BASE,
        ),
        ({"properties": {}}, None, _EXPECTED_TD_BASE),
    ],
    ids=[
        "required empty: False, not required empty: False",
        "required empty: False, not required empty: True",
        "required empty: True,  not required empty: False",
        "required empty: True,  not required empty: True",
    ],
)
@pytest.mark.models_file
def test_calculate_td_parent(
    schema, expected_required_parent, expected_not_required_parent
):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td required and not required parents are added to the
        artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.typed_dict.required.parent_class == expected_required_parent
    artifacts_not_required_parent = artifacts.typed_dict.not_required.parent_class
    assert artifacts_not_required_parent == expected_not_required_parent
