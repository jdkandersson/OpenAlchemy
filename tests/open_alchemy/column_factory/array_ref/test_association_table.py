"""Tests for array association table."""

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy.column_factory import array_ref


class TestGatherColumnArtifacts:
    """Tests for _gather_column_artifacts."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema",
        [
            {
                "x-tablename": "table 1",
                "properties": {"key": {"type": "integer", "x-primary-key": True}},
            },
            {
                "type": "not_object",
                "x-tablename": "table 1",
                "properties": {"key": {"type": "integer", "x-primary-key": True}},
            },
            {
                "type": "object",
                "properties": {"key": {"type": "integer", "x-primary-key": True}},
            },
            {"type": "object", "x-tablename": "table 1"},
            {"type": "object", "x-tablename": "table 1", "properties": {}},
            {
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"key": {"type": "integer"}},
            },
            {
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"key": {"x-primary-key": True}},
            },
            {
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"key": {"type": "object", "x-primary-key": True}},
            },
            {
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"key": {"type": "array", "x-primary-key": True}},
            },
            {
                "type": "object",
                "x-tablename": "table 1",
                "properties": {
                    "key_1": {"type": "simple_type", "x-primary-key": True},
                    "key_2": {"type": "simple_type", "x-primary-key": True},
                },
            },
        ],
        ids=[
            "type missing",
            "not object",
            "no tablename",
            "no properties",
            "properties empty",
            "no primary key",
            "primary key no type",
            "primary key object",
            "primary key array",
            "multiple primary key",
        ],
    )
    @pytest.mark.column
    def test_invalid(schema):
        """
        GIVEN invalid schema
        WHEN _gather_column_artifacts is called with the schema
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            array_ref._association_table._gather_column_artifacts(
                model_schema=schema, schemas={}
            )

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_format, expected_max_length",
        [
            (
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {
                        "key_1": {"type": "simple_type_1", "x-primary-key": True}
                    },
                },
                {},
                None,
                None,
            ),
            (
                {"$ref": "#/components/schemas/Schema"},
                {
                    "Schema": {
                        "type": "object",
                        "x-tablename": "table 1",
                        "properties": {
                            "key_1": {"type": "simple_type_1", "x-primary-key": True}
                        },
                    }
                },
                None,
                None,
            ),
            (
                {
                    "allOf": [
                        {
                            "type": "object",
                            "x-tablename": "table 1",
                            "properties": {
                                "key_1": {
                                    "type": "simple_type_1",
                                    "x-primary-key": True,
                                }
                            },
                        }
                    ]
                },
                {},
                None,
                None,
            ),
            (
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {"key_1": {"$ref": "#/components/schemas/Property"}},
                },
                {"Property": {"type": "simple_type_1", "x-primary-key": True}},
                None,
                None,
            ),
            (
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {
                        "key_1": {
                            "allOf": [{"type": "simple_type_1", "x-primary-key": True}]
                        }
                    },
                },
                {},
                None,
                None,
            ),
            (
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {
                        "key_1": {
                            "type": "simple_type_1",
                            "x-primary-key": True,
                            "format": "format 1",
                            "maxLength": 1,
                        }
                    },
                },
                {},
                "format 1",
                1,
            ),
            (
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {
                        "key_1": {
                            "type": "simple_type_1",
                            "x-primary-key": True,
                            "format": "format 1",
                            "maxLength": 1,
                        },
                        "key_2": {
                            "type": "simple_type_2",
                            "format": "format 2",
                            "maxLength": 2,
                        },
                    },
                },
                {},
                "format 1",
                1,
            ),
            (
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {
                        "key_2": {
                            "type": "simple_type_2",
                            "format": "format 2",
                            "maxLength": 2,
                        },
                        "key_1": {
                            "type": "simple_type_1",
                            "x-primary-key": True,
                            "format": "format 1",
                            "maxLength": 1,
                        },
                    },
                },
                {},
                "format 1",
                1,
            ),
        ],
        ids=[
            "plain",
            "$ref",
            "allOf",
            "property $ref",
            "property allOf",
            "property format",
            "multiple properties first",
            "multiple properties last",
        ],
    )
    @pytest.mark.column
    def test_valid(schema, schemas, expected_format, expected_max_length):
        """
        GIVEN schema, schemas and expected format, type, tablename and column name
        WHEN _gather_column_artifacts is called with the schema and schemas
        THEN the expected format, type, tablename and column name are returned.
        """
        expected_type = "simple_type_1"
        expected_tablename = "table 1"
        expected_column_name = "key_1"

        column = array_ref._association_table._gather_column_artifacts(
            model_schema=schema, schemas=schemas
        )

        assert column.type == expected_type
        assert column.format == expected_format
        assert column.tablename == expected_tablename
        assert column.column_name == expected_column_name
        assert column.max_length == expected_max_length


class TestConstructColumn:
    """Tests for _construct_column."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.column
    def test_column():
        """
        GIVEN many to many column artifacts
        WHEN _construct_column is called with the artifacts
        THEN a column is returned.
        """
        artifacts = array_ref._association_table._ColumnArtifacts(
            "integer", "int64", "table_1", "column_1", None
        )

        column = array_ref._association_table._construct_column(artifacts=artifacts)

        assert column.name == "table_1_column_1"
        assert isinstance(column.type, sqlalchemy.BigInteger)
        assert len(column.foreign_keys) == 1
        foreign_key = column.foreign_keys.pop()
        assert str(foreign_key) == "ForeignKey('table_1.column_1')"

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, max_length, expected_type",
        [
            ("integer", None, None, sqlalchemy.Integer),
            ("integer", "int64", None, sqlalchemy.BigInteger),
            ("string", None, None, sqlalchemy.String),
            ("string", None, 10, sqlalchemy.String),
        ],
        ids=["no format", "with format", "string no maxLength", "string maxLength"],
    )
    @pytest.mark.column
    def test_artifacts(type_, format_, max_length, expected_type):
        """
        GIVEN type, format, maxLength and expected type
        WHEN artifacts are constructed and _construct_column is called
        THEN a column with the expected type is returned.
        """
        artifacts = array_ref._association_table._ColumnArtifacts(
            type_, format_, "table_1", "column_1", max_length
        )

        column = array_ref._association_table._construct_column(artifacts=artifacts)

        assert isinstance(column.type, expected_type)
        if max_length is not None:
            assert column.type.length == max_length


@pytest.mark.column
def test_construct(mocked_facades_models):
    """
    GIVEN parent and child schema and tablename
    WHEN construct is called with the parent and child schema and
        tablename
    THEN a table with the correct name, columns and metadata is constructed.
    """
    # pylint: disable=protected-access,unsubscriptable-object
    parent_schema = {
        "type": "object",
        "x-tablename": "parent",
        "properties": {"parent_id": {"type": "integer", "x-primary-key": True}},
    }
    child_schema = {
        "type": "object",
        "x-tablename": "child",
        "properties": {"child_id": {"type": "string", "x-primary-key": True}},
    }
    tablename = "association"

    returned_table = array_ref._association_table.construct(
        parent_schema=parent_schema,
        child_schema=child_schema,
        schemas={},
        tablename=tablename,
    )

    assert returned_table.name == tablename
    assert returned_table.metadata == (
        mocked_facades_models.get_base.return_value.metadata
    )
    assert len(returned_table.columns) == 2
    assert isinstance(
        returned_table.columns["parent_parent_id"].type, sqlalchemy.Integer
    )
    assert isinstance(returned_table.columns["child_child_id"].type, sqlalchemy.String)
