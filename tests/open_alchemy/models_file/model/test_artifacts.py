"""Tests for artifacts."""
# pylint: disable=protected-access

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
    ],
    ids=["empty", "single", "multiple", "single in required", "single not in required"],
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

    assert artifacts.typed_dict.required_props == expected_props


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

    assert artifacts.typed_dict.not_required_props == expected_props


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

    assert artifacts.typed_dict.required_empty == expected_required_empty


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

    assert artifacts.typed_dict.not_required_empty == expected_not_required_empty


# Table for the name of the required and not required TypedDict names
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

    assert artifacts.typed_dict.required_name == expected_required_name
    assert artifacts.typed_dict.not_required_name == expected_not_required_name
