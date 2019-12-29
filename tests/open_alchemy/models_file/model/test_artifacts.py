"""Tests for artifacts."""
# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "schema, required, expected_artifacts",
    [
        (
            {"type": "type 1"},
            None,
            models_file.types.ColumnSchemaArtifacts(type="type 1"),
        ),
        (
            {"type": "type 1", "format": "format 1"},
            None,
            models_file.types.ColumnSchemaArtifacts(type="type 1", format="format 1"),
        ),
        (
            {"type": "type 1", "nullable": True},
            None,
            models_file.types.ColumnSchemaArtifacts(type="type 1", nullable=True),
        ),
        (
            {"type": "object", "x-de-$ref": "RefModel"},
            None,
            models_file.types.ColumnSchemaArtifacts(type="object", de_ref="RefModel"),
        ),
        (
            {"type": "array", "items": {"x-de-$ref": "RefModel"}},
            None,
            models_file.types.ColumnSchemaArtifacts(type="array", de_ref="RefModel"),
        ),
        (
            {"type": "type 1"},
            True,
            models_file.types.ColumnSchemaArtifacts(type="type 1", required=True),
        ),
    ],
    ids=[
        "type only",
        "type with format",
        "type with nullable",
        "object",
        "array",
        "required given",
    ],
)
@pytest.mark.models_file
def test_gather_column_artifacts(schema, required, expected_artifacts):
    """
    GIVEN schema and required
    WHEN gather_column_artifacts is called with the schema and required
    THEN the given expected artifacts are returned.
    """
    artifacts = models_file._model._artifacts.gather_column_artifacts(
        schema=schema, required=required
    )

    assert artifacts == expected_artifacts


@pytest.mark.models_file
def test_calculate_name():
    """
    GIVEN name
    WHEN calculate is called with the name
    THEN the name is added to the artifacts.
    """
    schema = {"properties": {}}
    name = "Model"

    artifacts = models_file._model._artifacts.calculate(schema=schema, name=name)

    assert artifacts.sqlalchemy.name == name


@pytest.mark.parametrize(
    "schema, expected_columns",
    [
        ({"properties": {}}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}},
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                )
            ],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                }
            },
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                ),
                models_file.types.ColumnArtifacts(
                    name="column_2", type="typing.Optional[str]"
                ),
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [models_file.types.ColumnArtifacts(name="column_1", type="int")],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                )
            ],
        ),
        ({"properties": {}, "x-backrefs": {}}, []),
        (
            {
                "properties": {},
                "x-backrefs": {"model": {"type": "object", "x-de-$ref": "Model"}},
            },
            [
                models_file.types.ColumnArtifacts(
                    name="model", type='typing.Optional["Model"]'
                )
            ],
        ),
        (
            {
                "properties": {},
                "x-backrefs": {
                    "model1": {"type": "object", "x-de-$ref": "Model1"},
                    "model2": {"type": "object", "x-de-$ref": "Model2"},
                },
            },
            [
                models_file.types.ColumnArtifacts(
                    name="model1", type='typing.Optional["Model1"]'
                ),
                models_file.types.ColumnArtifacts(
                    name="model2", type='typing.Optional["Model2"]'
                ),
            ],
        ),
    ],
    ids=[
        "empty",
        "single",
        "multiple",
        "single in required",
        "single not in required",
        "empty x-backrefs",
        "single x-backrefs",
        "multiple x-backrefs",
    ],
)
@pytest.mark.models_file
def test_calculate_column(schema, expected_columns):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected columns are added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.columns == expected_columns


@pytest.mark.parametrize(
    "schema, expected_empty",
    [
        ({"properties": {}}, True),
        ({"properties": {"column_1": {"type": "integer"}}}, False),
    ],
    ids=["empty", "single"],
)
@pytest.mark.models_file
def test_calculate_empty(schema, expected_empty):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected empty is added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.empty == expected_empty


@pytest.mark.parametrize(
    "schema, expected_props",
    [
        ({"properties": {}}, []),
        ({"properties": {"column_1": {"type": "integer"}}}, []),
        ({"properties": {"column_1": {"type": "integer"}}, "required": []}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [models_file.types.ColumnArtifacts(name="column_1", type="int")],
        ),
        (
            {
                "properties": {"column_1": {"type": "object", "x-de-$ref": "RefModel"}},
                "required": ["column_1"],
            },
            [models_file.types.ColumnArtifacts(name="column_1", type='"RefModelDict"')],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "str"},
                },
                "required": ["column_1", "column_2"],
            },
            [
                models_file.types.ColumnArtifacts(name="column_1", type="int"),
                models_file.types.ColumnArtifacts(name="column_2", type="str"),
            ],
        ),
    ],
    ids=[
        "empty",
        "single required not given",
        "single not required",
        "single required",
        "single required object",
        "multiple required",
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

    assert artifacts.typed_dict.required.props == expected_props


@pytest.mark.parametrize(
    "schema, expected_props",
    [
        ({"properties": {}}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}},
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                )
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                )
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [],
        ),
        (
            {
                "properties": {"column_1": {"type": "object", "x-de-$ref": "RefModel"}},
                "required": [],
            },
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type='typing.Optional["RefModelDict"]'
                )
            ],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "str"},
                },
                "required": [],
            },
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                ),
                models_file.types.ColumnArtifacts(
                    name="column_2", type="typing.Optional[str]"
                ),
            ],
        ),
    ],
    ids=[
        "empty",
        "single required not given",
        "single not required",
        "single required",
        "single not required object",
        "multiple not required",
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
def test_calculate_td_required_empty(schema, expected_required_empty):
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
def test_calculate_td_not_required_empty(schema, expected_not_required_empty):
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


_EXPECTED_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_BASE = "typing_extensions.TypedDict"


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
            _EXPECTED_BASE,
            "_ModelDictBase",
        ),
        (
            {"properties": {"column_1": {"type": "string"}}, "required": ["column_1"]},
            _EXPECTED_BASE,
            None,
        ),
        (
            {"properties": {"column_1": {"type": "string"}}, "required": []},
            None,
            _EXPECTED_BASE,
        ),
        ({"properties": {}}, None, _EXPECTED_BASE),
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
