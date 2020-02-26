"""Tests for array association table."""

import sys

import pytest

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
    def test_column(mocked_facades_sqlalchemy):
        """
        GIVEN many to many column artifacts
        WHEN _construct_column is called with the artifacts
        THEN sqlalchemy facade is called with the artifacts with the calculated foreign
            key.
        """
        artifacts = array_ref._association_table._ColumnArtifacts(
            "integer", "int64", "table_1", "column_1", None
        )

        column = array_ref._association_table._construct_column(artifacts=artifacts)

        # Check column construct call
        assert mocked_facades_sqlalchemy.column.construct.call_count == 1
        assert column == mocked_facades_sqlalchemy.column.construct.return_value
        assert column.name == "table_1_column_1"
        # Check call arguments
        if sys.version_info[1] == 8:
            kwargs = mocked_facades_sqlalchemy.column.construct.call_args.kwargs
        else:
            _, kwargs = mocked_facades_sqlalchemy.column.construct.call_args
        assert kwargs["artifacts"].open_api.type == "integer"
        assert kwargs["artifacts"].open_api.format == "int64"
        assert kwargs["artifacts"].extension.foreign_key == "table_1.column_1"

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, max_length",
        [
            ("integer", None, None),
            ("integer", "int64", None),
            ("string", None, None),
            ("string", None, 10),
        ],
        ids=["no format", "with format", "string no maxLength", "string maxLength"],
    )
    @pytest.mark.column
    def test_artifacts(type_, format_, max_length, mocked_facades_sqlalchemy):
        """
        GIVEN type, format, maxLength
        WHEN artifacts are constructed and _construct_column is called
        THEN the SQLAlchemy facade is called with the artifacts.
        """
        artifacts = array_ref._association_table._ColumnArtifacts(
            type_, format_, "table_1", "column_1", max_length
        )

        array_ref._association_table._construct_column(artifacts=artifacts)

        # Check call
        assert mocked_facades_sqlalchemy.column.construct.call_count == 1
        # Check call arguments
        if sys.version_info[1] == 8:
            kwargs = mocked_facades_sqlalchemy.column.construct.call_args.kwargs
        else:
            _, kwargs = mocked_facades_sqlalchemy.column.construct.call_args
        assert kwargs["artifacts"].open_api.type == type_
        assert kwargs["artifacts"].open_api.format == format_
        assert kwargs["artifacts"].open_api.max_length == max_length


@pytest.mark.column
def test_construct(mocked_facades_models, mocked_facades_sqlalchemy):
    """
    GIVEN parent and child schema and tablename
    WHEN construct is called with the parent and child schema and
        tablename
    THEN the SQLAlchemy facade is called with the artifacts extracted from the schema.
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

    # Check call
    assert mocked_facades_sqlalchemy.table.call_count == 1
    assert returned_table == mocked_facades_sqlalchemy.table.return_value
    # Check table call args
    if sys.version_info[1] == 8:
        kwargs = mocked_facades_sqlalchemy.table.call_args.kwargs
    else:
        _, kwargs = mocked_facades_sqlalchemy.table.call_args
    assert kwargs["tablename"] == tablename
    assert kwargs["base"] == mocked_facades_models.get_base.return_value
    assert len(kwargs["columns"]) == 2
    assert kwargs["columns"][0] == (
        mocked_facades_sqlalchemy.column.construct.return_value
    )
    assert kwargs["columns"][1] == (
        mocked_facades_sqlalchemy.column.construct.return_value
    )
    # Check column calls
    assert mocked_facades_sqlalchemy.column.construct.call_count == 2
    call_args_list = mocked_facades_sqlalchemy.column.construct.call_args_list
    if sys.version_info[1] == 8:
        kwargs = call_args_list[0].kwargs
    else:
        _, kwargs = call_args_list[0]
    assert kwargs["artifacts"].open_api.type == "integer"
    if sys.version_info[1] == 8:
        kwargs = call_args_list[1].kwargs
    else:
        _, kwargs = call_args_list[1]
    assert kwargs["artifacts"].open_api.type == "string"
