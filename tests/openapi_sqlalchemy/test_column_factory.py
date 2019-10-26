"""Tests for the column factory."""
# pylint: disable=protected-access

import typing

import pytest
import sqlalchemy

from openapi_sqlalchemy import column_factory
from openapi_sqlalchemy import exceptions


@pytest.mark.parametrize(
    "spec",
    [
        {"type": "object"},
        {"allOf": [{"type": "object"}]},
        {"allOf": [{"$ref": "ref 1"}, {"$ref": "ref 2"}]},
        {
            "allOf": [
                {"$ref": "ref 1"},
                {"x-backref": "backref 1"},
                {"x-backref": "backref 2"},
            ]
        },
    ],
    ids=[
        "object",
        "allOf with object",
        "allOf with multiple ref",
        "allOf with multiple x-backref",
    ],
)
@pytest.mark.column
def test_handle_object_error(spec):
    """
    GIVEN spec
    WHEN _handle_object is called with the spec
    THEN MalformedManyToOneRelationship is raised.
    """
    with pytest.raises(exceptions.MalformedManyToOneRelationship):
        column_factory._handle_object(
            spec=spec, schemas={}, required=True, logical_name="name 1"
        )


@pytest.mark.column
def test_spec_to_column_no_type():
    """
    GIVEN column schema without type
    WHEN column_factory is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        column_factory._spec_to_column(spec={})


@pytest.mark.column
def test_spec_to_column_type_unsupported():
    """
    GIVEN column schema with type that has not been implemented
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory._spec_to_column(spec={"type": "unsupported"})


@pytest.mark.column
def test_spec_to_column_column_return():
    """
    GIVEN valid schema
    WHEN column_factory is called with the schema
    THEN an instance of SQLAlchemy Column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "number"})

    assert isinstance(column, sqlalchemy.Column)


@pytest.mark.parametrize("primary_key", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_primary_key(primary_key: bool):
    """
    GIVEN valid schema and the value of the primary key property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column primary_key property is set to the input.
    """
    column = column_factory._spec_to_column(
        spec={"type": "number", "x-primary-key": primary_key}
    )

    assert column.primary_key == primary_key


@pytest.mark.parametrize("autoincrement", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_autoincrement(autoincrement: bool):
    """
    GIVEN valid schema and the value of the autoincrement property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column autoincrement property is set to the input.
    """
    column = column_factory._spec_to_column(
        spec={"type": "number", "x-autoincrement": autoincrement}
    )

    assert column.autoincrement == autoincrement


@pytest.mark.parametrize("index", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_index(index: bool):
    """
    GIVEN valid schema and the value of the index property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column index property is set to the input.
    """
    column = column_factory._spec_to_column(spec={"type": "number", "x-index": index})

    assert column.index == index


@pytest.mark.parametrize("unique", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_unique(unique: bool):
    """
    GIVEN valid schema and the value of the unique property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column unique property is set to the input.
    """
    column = column_factory._spec_to_column(spec={"type": "number", "x-unique": unique})

    assert column.unique == unique


@pytest.mark.column
def test_spec_to_column_foreign_key():
    """
    GIVEN valid schema which has x-foreign-key set
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column foreign key property is set.
    """
    column = column_factory._spec_to_column(
        spec={"type": "number", "x-foreign-key": "foreign.key"}
    )

    assert len(column.foreign_keys) == 1
    foreign_key = column.foreign_keys.pop()
    assert str(foreign_key) == "ForeignKey('foreign.key')"


@pytest.mark.parametrize(
    "required, nullable, expected",
    [
        (None, None, True),
        (None, False, False),
        (None, True, True),
        (False, None, True),
        (False, False, False),
        (False, True, True),
        (True, None, False),
        (True, False, False),
        (True, True, True),
    ],
    ids=[
        "required not given nullable not given",
        "required not given nullable reset",
        "required not given nullable set",
        "required reset nullable not given",
        "required reset nullable reset",
        "required reset nullable set",
        "required set nullable not given",
        "required set nullable reset",
        "required set nullable set",
    ],
)
@pytest.mark.column
def test_spec_to_column_nullable(
    required: typing.Optional[bool], nullable: typing.Optional[bool], expected: bool
):
    """
    GIVEN schema, the value for the nullable property and the required argument
    WHEN column_factory is called with the schema and required argument
    THEN SQLAlchemy column is returned where nullable property is equal to the
        expected input.
    """
    kwargs: typing.Dict[str, bool] = {}
    if required is not None:
        kwargs["required"] = required
    schema: typing.Dict[str, typing.Union[str, bool]] = {"type": "number"}
    if nullable is not None:
        schema["nullable"] = nullable
    column = column_factory._spec_to_column(spec=schema, **kwargs)

    assert column.nullable == expected


@pytest.mark.column
def test_spec_to_column_number():
    """
    GIVEN schema with number type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "number"})

    assert isinstance(column.type, sqlalchemy.Float)


@pytest.mark.column
def test_spec_to_column_number_float():
    """
    GIVEN schema with number type and float format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "number", "format": "float"})

    assert isinstance(column.type, sqlalchemy.Float)


@pytest.mark.column
def test_spec_to_column_number_double():
    """
    GIVEN schema with number type and double format
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory._spec_to_column(spec={"type": "number", "format": "double"})


@pytest.mark.column
def test_spec_to_column_number_unsupported_format():
    """
    GIVEN schema with number type and format that has not been implemented
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory._spec_to_column(spec={"type": "number", "format": "unsupported"})


@pytest.mark.column
def test_spec_to_column_integer():
    """
    GIVEN schema with integer type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "integer"})

    assert isinstance(column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_spec_to_column_integer_int32():
    """
    GIVEN schema with integer type and int32 format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "integer", "format": "int32"})

    assert isinstance(column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_spec_to_column_integer_int64():
    """
    GIVEN schema with integer type and int64 format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy BigInteger column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "integer", "format": "int64"})

    assert isinstance(column.type, sqlalchemy.BigInteger)


@pytest.mark.column
def test_spec_to_column_integer_unsupported_format():
    """
    GIVEN schema with integer type and unsupported format
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory._spec_to_column(
            spec={"type": "integer", "format": "unsupported"}
        )


@pytest.mark.column
def test_spec_to_column_string():
    """
    GIVEN schema with string type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy String column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "string"})

    assert isinstance(column.type, sqlalchemy.String)


@pytest.mark.column
def test_spec_to_column_string_length():
    """
    GIVEN schema with string type and maxLength property
    WHEN column_factory is called with the schema
    THEN SQLAlchemy String column is returned with the length set to the maxLength.
    """
    column = column_factory._spec_to_column(spec={"type": "string", "maxLength": 1})

    assert column.type.length == 1


@pytest.mark.column
def test_spec_to_column_boolean():
    """
    GIVEN schema with boolean type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy boolean column is returned.
    """
    column = column_factory._spec_to_column(spec={"type": "boolean"})

    assert isinstance(column.type, sqlalchemy.Boolean)


@pytest.mark.column
def test_handle_object_reference():
    """
    GIVEN
    WHEN _handle_object_reference is called
    THEN the function should exist.
    """
    assert hasattr(column_factory, "_handle_object_reference")


@pytest.mark.column
def test_handle_object_reference_no_tablename():
    """
    GIVEN object schema without x-tablename key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object_reference(
            spec={"properties": {"id": {}}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_no_properties():
    """
    GIVEN object schema without properties key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object_reference(
            spec={"x-tablename": "table 1"}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_id_missing():
    """
    GIVEN object schema without id in properties
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_id_no_type():
    """
    GIVEN object schema with id but no type for id
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {"id": {}}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_return():
    """
    GIVEN object schema with x-tablename and id property with a type
    WHEN _handle_object_reference is called with the schema
    THEN a schema with the type of the id property and x-foreign-key property.
    """
    spec = {"x-tablename": "table 1", "properties": {"id": {"type": "idType"}}}
    schemas = {}

    return_value = column_factory._handle_object_reference(spec=spec, schemas=schemas)

    assert return_value == {"type": "idType", "x-foreign-key": "table 1.id"}


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_ref():
    """
    GIVEN schema that references another schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"type": "boolean"}}
    [(logical_name, column)] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, sqlalchemy.Boolean)


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_ref():
    """
    GIVEN schema that references another object schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    [  # pylint: disable=unbalanced-tuple-unpacking
        (fk_logical_name, fk_column),
        (tbl_logical_name, relationship),
    ] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_ref_backref():
    """
    GIVEN schema that references another object schema which has x-backref and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship with backref is returned.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-backref": "backref 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    [  # pylint: disable=unbalanced-tuple-unpacking
        (fk_logical_name, fk_column),
        (tbl_logical_name, relationship),
    ] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref == "backref 1"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_ref():
    """
    GIVEN schema with allOf that references another object schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned.
    """
    spec = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    [  # pylint: disable=unbalanced-tuple-unpacking
        (fk_logical_name, fk_column),
        (tbl_logical_name, relationship),
    ] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_backref_ref():
    """
    GIVEN schema with allOf that references another object schema and has x-backref and
        schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship with backref is returned.
    """
    spec = {
        "allOf": [
            {"$ref": "#/components/schemas/RefSchema"},
            {"x-backref": "backref 1"},
        ]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    [  # pylint: disable=unbalanced-tuple-unpacking
        (fk_logical_name, fk_column),
        (tbl_logical_name, relationship),
    ] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref == "backref 1"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_backref_ref_backref():
    """
    GIVEN schema with allOf that references another object schema with backref and has
        x-backref and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship with backref from allOf is returned.
    """
    spec = {
        "allOf": [
            {"$ref": "#/components/schemas/RefSchema"},
            {"x-backref": "backref 2"},
        ]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-backref": "backref 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    [  # pylint: disable=unbalanced-tuple-unpacking
        (fk_logical_name, fk_column),
        (tbl_logical_name, relationship),
    ] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref == "backref 2"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_all_of():
    """
    GIVEN schema with allOf statement
    WHEN column_factory is called with the schema and schemas
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name.
    """
    spec = {"allOf": [{"type": "boolean"}]}
    schemas = {}
    [(logical_name, column)] = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, sqlalchemy.Boolean)
