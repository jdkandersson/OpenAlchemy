"""Tests for the column factory."""
# pylint: disable=protected-access

import copy

import pytest

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types
from open_alchemy.column_factory import column

OAColArt = types.OpenAPiColumnArtifacts
ExtColArt = types.ExtensionColumnArtifacts
ColArt = types.ColumnArtifacts


@pytest.mark.parametrize(
    "schema, expected_exception",
    [
        pytest.param(
            {},
            exceptions.TypeMissingError,
            id="type missing",
        ),
        pytest.param(
            {"type": 1},
            exceptions.TypeMissingError,
            id="type not string",
        ),
        pytest.param(
            {"type": "type 1", "format": 1},
            exceptions.MalformedSchemaError,
            id="format not string",
        ),
        pytest.param(
            {"type": "type 1", "maxLength": "1"},
            exceptions.MalformedSchemaError,
            id="maxLength not integer",
        ),
        pytest.param(
            {"type": "type 1", "nullable": "True"},
            exceptions.MalformedSchemaError,
            id="nullable not boolean",
        ),
        pytest.param(
            {"type": "type 1", "description": True},
            exceptions.MalformedSchemaError,
            id="description not string",
        ),
        pytest.param(
            {"type": "type 1", "x-primary-key": "True"},
            exceptions.MalformedExtensionPropertyError,
            id="primary key not boolean",
        ),
        pytest.param(
            {"type": "type 1", "x-autoincrement": "True"},
            exceptions.MalformedExtensionPropertyError,
            id="autoincrement not boolean",
        ),
        pytest.param(
            {"type": "type 1", "x-index": "True"},
            exceptions.MalformedExtensionPropertyError,
            id="index not boolean",
        ),
        pytest.param(
            {"type": "type 1", "x-unique": "True"},
            exceptions.MalformedExtensionPropertyError,
            id="unique not boolean",
        ),
        pytest.param(
            {"type": "type 1", "x-json": "True"},
            exceptions.MalformedExtensionPropertyError,
            id="json not boolean",
        ),
        pytest.param(
            {"type": "type 1", "x-foreign-key": True},
            exceptions.MalformedExtensionPropertyError,
            id="foreign key not string",
        ),
        pytest.param(
            {"type": "string", "default": 1},
            exceptions.MalformedSchemaError,
            id="default invalid",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {1: "value 1"}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs invalid",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"nullable": True}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs nullable",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"default": "value 1"}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs default",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"primary_key": True}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs primary_key",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"autoincrement": True}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs autoincrement",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"index": True}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs index",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"unique": True}},
            exceptions.MalformedExtensionPropertyError,
            id="kwargs unique",
        ),
        pytest.param(
            {"type": "string", "x-foreign-key-kwargs": {"key_1": "value 1"}},
            exceptions.MalformedSchemaError,
            id="fk kwargs no foreign key",
        ),
        pytest.param(
            {
                "type": "string",
                "x-foreign-key": "table.column",
                "x-foreign-key-kwargs": {1: "value 1"},
            },
            exceptions.MalformedExtensionPropertyError,
            id="fk kwargs invalid",
        ),
    ],
)
@pytest.mark.column
def test_check_schema_invalid(schema, expected_exception):
    """
    GIVEN invalid schema
    WHEN check_schema is called with the schema
    THEN given exception is raised.
    """
    with pytest.raises(expected_exception):
        column.check_schema(schema=schema)


@pytest.mark.parametrize(
    "schema, expected_artifacts",
    [
        pytest.param(
            {"type": "type 1"}, ColArt(open_api=OAColArt(type="type 1")), id="type only"
        ),
        pytest.param(
            {"type": "type 1", "format": "format 1"},
            ColArt(open_api=OAColArt(type="type 1", format="format 1")),
            id="format",
        ),
        pytest.param(
            {"type": "type 1", "maxLength": 1},
            ColArt(open_api=OAColArt(type="type 1", max_length=1)),
            id="maxLength",
        ),
        pytest.param(
            {"type": "type 1", "nullable": True},
            ColArt(open_api=OAColArt(type="type 1", nullable=True)),
            id="nullable",
        ),
        pytest.param(
            {"type": "type 1", "description": "description 1"},
            ColArt(open_api=OAColArt(type="type 1", description="description 1")),
            id="description",
        ),
        pytest.param(
            {"type": "type 1", "x-primary-key": True},
            ColArt(
                open_api=OAColArt(type="type 1"), extension=ExtColArt(primary_key=True)
            ),
            id="primary key",
        ),
        pytest.param(
            {"type": "type 1", "x-autoincrement": True},
            ColArt(
                open_api=OAColArt(type="type 1", nullable=False),
                extension=ExtColArt(autoincrement=True),
            ),
            id="autoincrement",
        ),
        pytest.param(
            {"type": "type 1", "x-index": True},
            ColArt(open_api=OAColArt(type="type 1"), extension=ExtColArt(index=True)),
            id="index",
        ),
        pytest.param(
            {"type": "type 1", "x-unique": True},
            ColArt(open_api=OAColArt(type="type 1"), extension=ExtColArt(unique=True)),
            id="unique",
        ),
        pytest.param(
            {"type": "type 1", "x-json": True},
            ColArt(open_api=OAColArt(type="type 1"), extension=ExtColArt(json=True)),
            id="json",
        ),
        pytest.param(
            {"type": "type 1", "x-foreign-key": "table.column"},
            ColArt(
                open_api=OAColArt(type="type 1"),
                extension=ExtColArt(foreign_key="table.column"),
            ),
            id="foreign key",
        ),
        pytest.param(
            {"type": "string", "default": "value 1"},
            ColArt(open_api=OAColArt(type="string", default="value 1", nullable=False)),
            id="default",
        ),
        pytest.param(
            {"type": "string", "x-kwargs": {"key_1": "value 1"}},
            ColArt(
                open_api=OAColArt(type="string"),
                extension=ExtColArt(kwargs={"key_1": "value 1"}),
            ),
            id="kwargs",
        ),
        pytest.param(
            {
                "type": "string",
                "x-foreign-key": "table.column",
                "x-foreign-key-kwargs": {"key_1": "value 1"},
            },
            ColArt(
                open_api=OAColArt(type="string"),
                extension=ExtColArt(
                    foreign_key="table.column", foreign_key_kwargs={"key_1": "value 1"}
                ),
            ),
            id="foreign key kwargs",
        ),
        pytest.param(
            {"type": "type 1", "readOnly": True},
            ColArt(open_api=OAColArt(type="type 1", read_only=True)),
            id="readOnly",
        ),
        pytest.param(
            {"type": "type 1", "writeOnly": True},
            ColArt(open_api=OAColArt(type="type 1", write_only=True)),
            id="writeOnly",
        ),
    ],
)
@pytest.mark.column
def test_check_schema_artifacts(schema, expected_artifacts):
    """
    GIVEN schema and expected artifacts
    WHEN check_schema is called with the schema
    THEN the expected artifacts are returned.
    """
    artifacts = column.check_schema(schema=schema)

    assert artifacts == expected_artifacts


@pytest.mark.column
def test_check_schema_required():
    """
    GIVEN schema
    WHEN check_schema is called with the schema and required True
    THEN nullable is False.
    """
    schema = {"type": "type 1"}

    artifacts = column.check_schema(schema=copy.deepcopy(schema), required=True)

    assert artifacts.open_api.nullable is False


@pytest.mark.parametrize(
    "artifacts, nullable, dict_ignore, expected_schema",
    [
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1")),
            None,
            None,
            {"type": "type 1"},
            id="type only",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", format="format 1")),
            None,
            None,
            {"type": "type 1", "format": "format 1"},
            id="type with format",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", max_length=1)),
            None,
            None,
            {"type": "type 1", "maxLength": 1},
            id="type with maxLength",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", description="description 1")),
            None,
            None,
            {"type": "type 1", "description": "description 1"},
            id="type with description",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", nullable=False)),
            None,
            None,
            {"type": "type 1"},
            id="type with nullable",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1"), extension=ExtColArt(json=True)),
            None,
            None,
            {"type": "type 1", "x-json": True},
            id="type with x-json",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", default="value 1")),
            None,
            None,
            {"type": "type 1", "default": "value 1"},
            id="type with default",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", read_only=True)),
            None,
            None,
            {"type": "type 1", "readOnly": True},
            id="type with readOnly",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1", write_only=True)),
            None,
            None,
            {"type": "type 1", "writeOnly": True},
            id="type with writeOnly",
        ),
        pytest.param(
            ColArt(
                open_api=OAColArt(type="type 1"),
                extension=ExtColArt(autoincrement=True),
            ),
            None,
            None,
            {"type": "type 1", "x-generated": True},
            id="type with autoincrement",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1")),
            False,
            None,
            {"type": "type 1", "nullable": False},
            id="nullable input not None",
        ),
        pytest.param(
            ColArt(open_api=OAColArt(type="type 1")),
            None,
            True,
            {"type": "type 1", "x-dict-ignore": True},
            id="dict_ignore input not None",
        ),
    ],
)
@pytest.mark.column
def test_calculate_schema(artifacts, expected_schema, nullable, dict_ignore):
    """
    GIVEN schema
    WHEN calculate_schema is called with the schema
    THEN the schema is returned.
    """
    returned_schema = column.calculate_schema(
        artifacts=artifacts, nullable=nullable, dict_ignore=dict_ignore
    )

    assert returned_schema == expected_schema


@pytest.mark.parametrize(
    "artifacts, expected_schema",
    [
        (ColArt(open_api=OAColArt(type="type 1")), {"type": "type 1"}),
        (
            ColArt(open_api=OAColArt(type="type 1")),
            {"type": "type 1", "nullable": True},
        ),
        (
            ColArt(open_api=OAColArt(type="type 1")),
            {"type": "type 1", "x-dict-ignore": True},
        ),
    ],
    ids=["type only", "type with nullable", "type with x-dict-ignore"],
)
@pytest.mark.column
def test_calculate_column_schema(artifacts, expected_schema):
    """
    GIVEN schema
    WHEN _calculate_column_schema is called with the schema
    THEN the schema is returned.
    """
    returned_schema = column._calculate_column_schema(
        artifacts=artifacts, schema=copy.deepcopy(expected_schema), schemas={}
    )

    assert returned_schema == expected_schema


@pytest.mark.column
def test_calculate_column_schema_dict_ignore_invalid():
    """
    GIVEN schema with invalid x-dict-ignore
    WHEN _calculate_column_schema is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        column._calculate_column_schema(
            artifacts=ColArt(open_api=OAColArt(type="type 1")),
            schema={"type": "type 1", "x-dict-ignore": "True"},
            schemas={},
        )


@pytest.mark.column
def test_calculate_column_schema_json():
    """
    GIVEN schema
    WHEN _calculate_column_schema is called with the schema
    THEN the schema is returned.
    """
    artifacts = ColArt(open_api=OAColArt(type="type 1"), extension=ExtColArt(json=True))
    schema = {
        "type": "object",
        "properties": {"column": {"$ref": "#/components/schemas/RefSchema"}},
    }
    schemas = {"RefSchema": {"type": "integer"}}

    returned_schema = column._calculate_column_schema(
        artifacts=artifacts, schema=schema, schemas=schemas
    )

    assert returned_schema == {
        "type": "object",
        "properties": {"column": {"type": "integer"}},
    }


class TestCheckArtifacts:
    """Tests for _check_artifacts."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, max_length, autoincrement",
        [
            pytest.param(
                "integer",
                None,
                1,
                None,
                id="maxLength integer",
            ),
            pytest.param(
                "number",
                None,
                1,
                None,
                id="maxLength number",
            ),
            pytest.param(
                "boolean",
                None,
                1,
                None,
                id="maxLength boolean",
            ),
            pytest.param(
                "string",
                "date",
                1,
                None,
                id="maxLength string  date",
            ),
            pytest.param(
                "string",
                "date-time",
                1,
                None,
                id="maxLength string date-time",
            ),
            pytest.param(
                "number",
                None,
                None,
                True,
                id="autoincrement number",
            ),
            pytest.param(
                "string",
                None,
                None,
                True,
                id="autoincrement string",
            ),
            pytest.param(
                "boolean",
                None,
                None,
                True,
                id="autoincrement boolean",
            ),
            pytest.param(
                "boolean",
                "format1",
                None,
                None,
                id="format boolean",
            ),
        ],
    )
    @pytest.mark.column
    def test_invalid(type_, format_, max_length, autoincrement):
        """
        GIVEN type, format, maxLength and autoincrement
        WHEN _check_artifacts is called with the artifacts
        THEN MalformedSchemaError is raised.
        """
        artifacts = ColArt(
            open_api=OAColArt(type=type_, format=format_, max_length=max_length),
            extension=ExtColArt(autoincrement=autoincrement),
        )

        with pytest.raises(exceptions.MalformedSchemaError):
            column._check_artifacts(artifacts=artifacts)

    @staticmethod
    @pytest.mark.column
    def test_invalid_json_default():
        """
        GIVEN JSON column with default
        WHEN _check_artifacts is called
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = ColArt(
            open_api=OAColArt(type="type 1", default="value 1"),
            extension=ExtColArt(json=True),
        )

        with pytest.raises(exceptions.FeatureNotImplementedError):
            column._check_artifacts(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, max_length, autoincrement",
        [
            ("string", None, 1, None),
            ("string", "byte", 1, None),
            ("string", "password", 1, None),
            ("string", "binary", 1, None),
            ("integer", None, None, True),
            ("integer", "int32", None, None),
            ("number", "float", None, None),
            ("string", "password", None, None),
        ],
        ids=[
            "maxLength     string",
            "maxLength     string  byte",
            "maxLength     string  password",
            "maxLength     string  binary",
            "autoincrement integer",
            "format        integer",
            "format        number",
            "format        string",
        ],
    )
    @pytest.mark.column
    def test_valid(type_, format_, max_length, autoincrement):
        """
        GIVEN valid artifacts
        WHEN _check_artifacts is called
        THEN MalformedSchemaError is not raised.
        """
        artifacts = ColArt(
            open_api=OAColArt(type=type_, format=format_, max_length=max_length),
            extension=ExtColArt(autoincrement=autoincrement),
        )

        column._check_artifacts(artifacts=artifacts)


@pytest.mark.column
def test_construct_column_invalid():
    """
    GIVEN artifacts that are not valid
    WHEN construct_column is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = ColArt(
        open_api=OAColArt(type="string"), extension=ExtColArt(autoincrement=True)
    )

    with pytest.raises(exceptions.MalformedSchemaError):
        column.construct_column(artifacts=artifacts)


@pytest.mark.column
def test_construct_column_valid():
    """
    GIVEN artifacts that are not valid
    WHEN construct_column is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = ColArt(open_api=OAColArt(type="string"))

    return_column = column.construct_column(artifacts=artifacts)

    assert isinstance(return_column, facades.sqlalchemy.column.Column)
    assert isinstance(return_column.type, facades.sqlalchemy.column.String)


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle_column is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    returned_column, returned_schema = column.handle_column(
        schema={"$ref": "#/components/schemas/Column"},
        schemas={"Column": {"type": "number"}},
    )

    assert isinstance(returned_column, facades.sqlalchemy.column.Column)
    assert isinstance(returned_column.type, facades.sqlalchemy.column.Number)
    assert returned_schema == {"type": "number"}
