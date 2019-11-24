"""Tests for array references."""

import sys
from unittest import mock

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy.column_factory import array_ref


@pytest.mark.parametrize(
    "spec, schemas",
    [
        ({"type": "array"}, {}),
        ({"type": "array", "items": {}}, {}),
        ({"type": "array", "items": {"allOf": []}}, {}),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "ref 1"}, {"$ref": "ref 2"}]},
            },
            {},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {"RefSchema": {}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "integer"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "x-backref": "schema",
                    "x-uselist": False,
                }
            },
        ),
    ],
    ids=[
        "no items",
        "items without $ref and allOf",
        "items allOf without $ref",
        "items allOf multiple $ref",
        "$ref items no type",
        "allOf items no type",
        "items type not object",
        "items no x-tablename",
        "backref and uselist defined",
    ],
)
@pytest.mark.column
def test_handle_array_invalid(spec, schemas):
    """
    GIVEN array schema that is not valid and schemas
    WHEN handle_array is called
    THEN MalformedRelationshipError is raised.
    """
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref.handle_array(
            spec=spec,
            model_schema=model_schema,
            schemas=schemas,
            logical_name="ref_schema",
        )


@pytest.mark.parametrize(
    "spec, schemas",
    [
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                },
            },
        ),
        (
            {
                "allOf": [
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                ]
            },
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "allOf": [
                        {
                            "type": "object",
                            "x-tablename": "ref_schema",
                            "properties": {},
                        }
                    ]
                }
            },
        ),
    ],
    ids=[
        "array items $ref",
        "$ref array items $ref",
        "allOf array items $ref",
        "array items allOf $ref",
        "array items $ref allOf",
    ],
)
@pytest.mark.column
def test_handle_array_relationship(spec, schemas):
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN relationship is returned pointing to the referenced schema.
    """
    logical_name = "ref_schema"
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    ([(tbl_logical_name, relationship)], schema_spec) = array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name=logical_name
    )

    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.secondary is None
    assert tbl_logical_name == logical_name
    assert schema_spec == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }


@pytest.mark.column
def test_handle_array_relationship_backref():
    """
    GIVEN schema with array referencing another schema with backref and schemas
    WHEN handle_array is called
    THEN relationship with backref is returned.
    """
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "x-backref": "schema",
            "properties": {},
        }
    }
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    ([(_, relationship)], _) = array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert relationship.backref == "schema"


@pytest.mark.column
def test_handle_array_relationship_secondary(_mocked_facades_models):
    """
    GIVEN schema with array referencing another schema with secondary and schemas
    WHEN handle_array is called
    THEN relationship with secondary is returned.
    """
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "x-secondary": "association",
            "properties": {"id": {"type": "integer", "x-primary-key": True}},
        }
    }
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer", "x-primary-key": True}},
    }

    ([(_, relationship)], _) = array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert relationship.secondary == "association"


@pytest.mark.column
def test_handle_array_schemas():
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN foreign key is added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {"type": "object", "x-tablename": "ref_schema", "properties": {}},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_id": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.id",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_handle_array_schemas_fk_def():
    """
    GIVEN schema with array referencing another schema which already has foreign key
        and schemas
    WHEN handle_array is called
    THEN foreign key is not added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {
                "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
            },
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {
                "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
            },
        }
    }


@pytest.mark.column
def test_handle_array_schemas_fk_def_all_of():
    """
    GIVEN schema with array referencing another schema which has allOf which already
        has foreign key and schemas
    WHEN handle_array is called
    THEN foreign key is not added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {
                        "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
                    },
                }
            ]
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {
                        "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
                    },
                }
            ]
        }
    }


@pytest.mark.column
def test_handle_array_schemas_foreign_key_column():
    """
    GIVEN schema with array referencing another schema with foreign key and schemas
    WHEN handle_array is called
    THEN foreign key is added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"fk_column": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "x-foreign-key-column": "fk_column",
            "properties": {},
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "x-foreign-key-column": "fk_column",
                    "properties": {},
                },
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_fk_column": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.fk_column",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_handle_array_secondary(mocked_facades_models):
    """
    GIVEN schema with array referencing another schema and secondary set and schemas
    WHEN handle_array is called
    THEN table is set on models.
    """
    secondary = "association"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer", "x-primary-key": True}},
    }
    spec = {
        "type": "array",
        "items": {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-secondary": secondary},
            ]
        },
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer", "x-primary-key": True}},
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert mocked_facades_models.set_association.call_count == 1
    if sys.version_info[1] == 8:
        name = mocked_facades_models.set_association.call_args.kwargs["name"]
        table = mocked_facades_models.set_association.call_args.kwargs["table"]
    else:
        _, kwargs = mocked_facades_models.set_association.call_args
        name = kwargs["name"]
        table = kwargs["table"]
    assert name == secondary
    assert table.name == secondary


@pytest.mark.column
def test_set_foreign_key_schemas_missing():
    """
    GIVEN referenced model is not in models and not in schemas
    WHEN _set_foreign_key is called with the referenced model name
    THEN MalformedRelationshipError is raised.
    """
    fk_column = "column_1"
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {fk_column: {"type": "integer"}},
    }

    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref._set_foreign_key(  # pylint: disable=protected-access
            ref_model_name="RefSchema",
            model_schema=model_schema,
            schemas={},
            fk_column=fk_column,
        )


@pytest.mark.column
def test_set_foreign_key_schemas():
    """
    GIVEN referenced model is not in models, model schema, schemas and foreign key
        column
    WHEN _set_foreign_key is called with the model schema, schemas and foreign key
        column
    THEN the foreign key column is added to the referenced model using allOf.
    """
    ref_model_name = "RefSchema"
    fk_column = "column_1"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {fk_column: {"type": "integer"}},
    }
    schemas = {ref_model_name: {"type": "object", "properties": {}}}

    array_ref._set_foreign_key(  # pylint: disable=protected-access
        ref_model_name=ref_model_name,
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    assert schemas == {
        ref_model_name: {
            "allOf": [
                {"type": "object", "properties": {}},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_{fk_column}": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.{fk_column}",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_set_foreign_key_models(mocked_facades_models: mock.MagicMock):
    """
    GIVEN mocked models, referenced model is in models, model schema, schemas and
        foreign key column
    WHEN _set_foreign_key is called with the model schema, schemas and foreign key
        column
    THEN the foreign key is added to the model.
    """
    ref_model_name = "RefSchema"
    fk_column = "column_1"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {fk_column: {"type": "integer"}},
    }
    schemas = {ref_model_name: {"type": "object", "properties": {}}}
    mock_ref_model = mock.MagicMock()
    mocked_facades_models.get_model.return_value = mock_ref_model

    array_ref._set_foreign_key(  # pylint: disable=protected-access
        ref_model_name=ref_model_name,
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    added_fk_column = getattr(mock_ref_model, f"{tablename}_{fk_column}")
    assert isinstance(added_fk_column.type, sqlalchemy.Integer)
    foreign_key = list(added_fk_column.foreign_keys)[0]
    assert f"{tablename}.{fk_column}" in str(foreign_key)
    mocked_facades_models.get_model.assert_called_once_with(name=ref_model_name)


class TestManyToManyColumnArtifacts:
    """Tests for _many_to_many_column_artifacts."""

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
        WHEN _many_to_many_column_artifacts is called with the schema
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            array_ref._many_to_many_column_artifacts(model_schema=schema, schemas={})

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
        WHEN _many_to_many_column_artifacts is called with the schema and schemas
        THEN the expected format, type, tablename and column name are returned.
        """
        expected_type = "simple_type_1"
        expected_tablename = "table 1"
        expected_column_name = "key_1"

        column = array_ref._many_to_many_column_artifacts(
            model_schema=schema, schemas=schemas
        )

        assert column.type_ == expected_type
        assert column.format_ == expected_format
        assert column.tablename == expected_tablename
        assert column.column_name == expected_column_name
        assert column.max_length == expected_max_length


class TestManyToManyColumn:
    """Tests for _many_to_many_column."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.column
    def test_column():
        """
        GIVEN many to many column artifacts
        WHEN _many_to_many_column is called with the artifacts
        THEN a column is returned.
        """
        artifacts = array_ref._ManyToManyColumnArtifacts(
            "integer", "int64", "table_1", "column_1", None
        )

        column = array_ref._many_to_many_column(artifacts=artifacts)

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
            ("integer", "int32", None, sqlalchemy.Integer),
            ("integer", "int64", None, sqlalchemy.BigInteger),
            ("number", None, None, sqlalchemy.Float),
            ("number", "float", None, sqlalchemy.Float),
            ("string", None, None, sqlalchemy.String),
            ("string", None, 10, sqlalchemy.String),
            ("boolean", None, None, sqlalchemy.Boolean),
        ],
        ids=[
            "integer no format",
            "integer 32 bit format",
            "integer 64 bit format",
            "number no format",
            "number format",
            "string no maxLength",
            "string maxLength",
            "boolean",
        ],
    )
    @pytest.mark.column
    def test_types(type_, format_, max_length, expected_type):
        """
        GIVEN type, format, maxLength and expected type
        WHEN artifacts are constructed and _many_to_many_column is called
        THEN a column with the expected type is returned.
        """
        artifacts = array_ref._ManyToManyColumnArtifacts(
            type_, format_, "table_1", "column_1", max_length
        )

        column = array_ref._many_to_many_column(artifacts=artifacts)

        assert isinstance(column.type, expected_type)


@pytest.mark.column
def test_construct_association_table(mocked_facades_models):
    """
    GIVEN parent and child schema and tablename
    WHEN _construct_association_table is called with the parent and child schema and
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

    returned_table = array_ref._construct_association_table(
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
