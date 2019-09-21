"""Tests for the column factory."""
# pylint: disable=protected-access

import typing
from unittest import mock

import pytest
import sqlalchemy

from openapi_sqlalchemy import column_factory
from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import types


@pytest.mark.prod_env
@pytest.mark.column
def test_resolve_ref_resolve_ref_call(mocked_resolve_ref: mock.MagicMock):
    """
    GIVEN mock function, mocked resolve_ref helper, spec, schemas and logical name
    WHEN mock function is decorated with resolve_ref and called with spec, schemas,
        and logical name
    THEN mocked resolve_ref helper is called with the schema based on spec and logical
        name and schemas.
    """
    mock_func = mock.MagicMock()
    spec = mock.MagicMock()
    schemas = mock.MagicMock()
    logical_name = mock.MagicMock()

    decorated = column_factory.resolve_ref(mock_func)
    decorated(spec=spec, schemas=schemas, logical_name=logical_name)

    schema = types.Schema(spec=spec, logical_name=logical_name)
    mocked_resolve_ref.assert_called_once_with(schema=schema, schemas=schemas)


@pytest.mark.prod_env
@pytest.mark.column
def test_resolve_ref_call(mocked_resolve_ref: mock.MagicMock, kwargs):
    """
    GIVEN mock function, mocked resolve_ref helper, spec, schemas, logical name and
        kwargs
    WHEN mock function is decorated with resolve_ref and called with spec, schemas,
        logical name and kwargs
    THEN mock function is called with logical name and spec from resolve_ref helper
        return value.
    """
    mock_func = mock.MagicMock()
    spec = mock.MagicMock()
    schemas = mock.MagicMock()
    logical_name = mock.MagicMock()

    decorated = column_factory.resolve_ref(mock_func)
    decorated(spec=spec, schemas=schemas, logical_name=logical_name, **kwargs)

    mock_func.assert_called_once_with(
        spec=mocked_resolve_ref.return_value.spec,
        logical_name=logical_name,
        schemas=schemas,
        **kwargs,
    )


@pytest.mark.prod_env
@pytest.mark.column
def test_resolve_ref_return(mocked_resolve_ref: mock.MagicMock):
    """
    GIVEN mock function, spec, schemas and logical name
    WHEN mock function is decorated with resolve_ref and called with schema, schemas
        and logical name
    THEN mock function return value is returned.
    """
    # pylint: disable=unused-argument
    mock_func = mock.MagicMock()
    spec = mock.MagicMock()
    schemas = mock.MagicMock()
    logical_name = mock.MagicMock()

    decorated = column_factory.resolve_ref(mock_func)
    return_value = decorated(spec=spec, schemas=schemas, logical_name=logical_name)

    assert return_value == mock_func.return_value


@pytest.mark.prod_env
@pytest.mark.column
def test_resolve_ref_object_call(mocked_resolve_ref: mock.MagicMock, kwargs):
    """
    GIVEN mock function and mocked resolve_ref helper that returns object spec
    WHEN mock function is decorated with resolve_ref and called
    THEN mock function is called with the object's id schema.
    """
    mock_func = mock.MagicMock()
    spec = mock.MagicMock()
    schemas = mock.MagicMock()
    logical_name = "logical name 1"
    mocked_resolve_ref.side_effect = [
        types.Schema(
            logical_name="name 1",
            spec={
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"id": {"type": "boolean"}},
            },
        ),
        types.Schema(
            logical_name="id", spec={"type": "boolean", "x-foreign-key": "table 1.id"}
        ),
    ]

    decorated = column_factory.resolve_ref(mock_func)
    decorated(spec=spec, schemas=schemas, logical_name=logical_name, **kwargs)

    mock_func.assert_called_once_with(
        spec={"type": "boolean", "x-foreign-key": "table 1.id"},
        logical_name="logical name 1_id",
        schemas=schemas,
        **kwargs,
    )


@pytest.mark.prod_env
@pytest.mark.column
def test_resolve_ref_object_relationship_call(
    mocked_resolve_ref: mock.MagicMock, mocked_sqlalchemy_relationship: mock.MagicMock
):
    """
    GIVEN mock function, mocked resolve_ref helper that returns object spec and mocked
        sqlalchemy.orm.relationship
    WHEN mock function is decorated with resolve_ref and called
    THEN sqlalchemy.orm.relationship is called with object logical name.
    """
    mock_func = mock.MagicMock()
    spec = mock.MagicMock()
    schemas = mock.MagicMock()
    logical_name = "logical name 1"
    mocked_resolve_ref.side_effect = [
        types.Schema(
            logical_name="name 1",
            spec={
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"id": {"type": "boolean"}},
            },
        ),
        types.Schema(
            logical_name="id", spec={"type": "boolean", "x-foreign-key": "table 1.id"}
        ),
    ]

    decorated = column_factory.resolve_ref(mock_func)
    decorated(spec=spec, schemas=schemas, logical_name=logical_name)

    mocked_sqlalchemy_relationship.assert_called_once_with("name 1")


@pytest.mark.prod_env
@pytest.mark.column
def test_resolve_ref_object_return(
    mocked_resolve_ref: mock.MagicMock, mocked_sqlalchemy_relationship: mock.MagicMock
):
    """
    GIVEN mock function and mocked resolve_ref helper that returns object spec
    WHEN mock function is decorated with resolve_ref and called
    THEN mock function return together with relationship is returned.
    """
    mock_func = mock.MagicMock()
    spec = mock.MagicMock()
    schemas = mock.MagicMock()
    logical_name = "logical name 1"
    mocked_resolve_ref.side_effect = [
        types.Schema(
            logical_name="name 1",
            spec={
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"id": {"type": "boolean"}},
            },
        ),
        types.Schema(
            logical_name="id", spec={"type": "boolean", "x-foreign-key": "table 1.id"}
        ),
    ]

    decorated = column_factory.resolve_ref(mock_func)
    return_value = decorated(spec=spec, schemas=schemas, logical_name=logical_name)

    mock_func.return_value.append.assert_called_once_with(
        (logical_name, mocked_sqlalchemy_relationship.return_value)
    )
    assert return_value == mock_func.return_value


@pytest.mark.prod_env
@pytest.mark.column
def test_merge_all_of_merge_all_of_call(mocked_merge_all_of: mock.MagicMock):
    """
    GIVEN mock function, mocked merge_all_of helper, mock spec and schemas
    WHEN mock function is decorated with merge_all_of and called with spec, schemas
    THEN merge_all_of helper is called with the spec and schemas.
    """
    mock_func = mock.MagicMock()
    mock_spec = mock.MagicMock()
    mock_schemas = mock.MagicMock()

    decorated = column_factory.merge_all_of(mock_func)
    decorated(spec=mock_spec, schemas=mock_schemas)

    mocked_merge_all_of.assert_called_once_with(spec=mock_spec, schemas=mock_schemas)


@pytest.mark.prod_env
@pytest.mark.column
def test_merge_all_of_call(mocked_merge_all_of: mock.MagicMock, kwargs):
    """
    GIVEN mock function, mocked merge_all_of helper and kwargs
    WHEN mock function is decorated with merge_all_of and called with kwargs
    THEN mock function is called with merge_all_of helper return value as spec and
        kwargs.
    """
    mock_func = mock.MagicMock()

    decorated = column_factory.merge_all_of(mock_func)
    decorated(spec=mock.MagicMock(), schemas=mock.MagicMock(), **kwargs)

    mock_func.assert_called_once_with(spec=mocked_merge_all_of.return_value, **kwargs)


@pytest.mark.prod_env
@pytest.mark.column
def test_merge_all_of_return(mocked_merge_all_of):  # pylint: disable=unused-argument
    """
    GIVEN mock function
    WHEN mock function is decorated with merge_all_of and called
    THEN mock function return value is returned.
    """
    mock_func = mock.MagicMock()

    decorated = column_factory.merge_all_of(mock_func)
    return_value = decorated(spec=mock.MagicMock(), schemas=mock.MagicMock())

    assert return_value == mock_func.return_value


@pytest.mark.column
def test_no_type():
    """
    GIVEN column schema without type
    WHEN column_factory is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        column_factory.column_factory(spec={})


@pytest.mark.column
def test_type_unsupported():
    """
    GIVEN column schema with type that has not been implemented
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory.column_factory(spec={"type": "unsupported"})


@pytest.mark.column
def test_column_return():
    """
    GIVEN valid schema
    WHEN column_factory is called with the schema
    THEN an instance of SQLAlchemy Column is returned.
    """
    column = column_factory.column_factory(spec={"type": "number"})

    assert isinstance(column, sqlalchemy.Column)


@pytest.mark.parametrize("primary_key", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_primary_key(primary_key: bool):
    """
    GIVEN valid schema and the value of the primary key property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column primary_key property is set to the input.
    """
    column = column_factory.column_factory(
        spec={"type": "number", "x-primary-key": primary_key}
    )

    assert column.primary_key == primary_key


@pytest.mark.parametrize("autoincrement", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_autoincrement(autoincrement: bool):
    """
    GIVEN valid schema and the value of the autoincrement property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column autoincrement property is set to the input.
    """
    column = column_factory.column_factory(
        spec={"type": "number", "x-autoincrement": autoincrement}
    )

    assert column.autoincrement == autoincrement


@pytest.mark.parametrize("index", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_index(index: bool):
    """
    GIVEN valid schema and the value of the index property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column index property is set to the input.
    """
    column = column_factory.column_factory(spec={"type": "number", "x-index": index})

    assert column.index == index


@pytest.mark.parametrize("unique", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_unique(unique: bool):
    """
    GIVEN valid schema and the value of the unique property
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column unique property is set to the input.
    """
    column = column_factory.column_factory(spec={"type": "number", "x-unique": unique})

    assert column.unique == unique


@pytest.mark.column
def test_foreign_key():
    """
    GIVEN valid schema which has x-foreign-key set
    WHEN column_factory is called with the schema
    THEN the returned SQLAlchemy column foreign key property is set.
    """
    column = column_factory.column_factory(
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
def test_nullable(
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
    column = column_factory.column_factory(spec=schema, **kwargs)

    assert column.nullable == expected


@pytest.mark.column
def test_number():
    """
    GIVEN schema with number type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    column = column_factory.column_factory(spec={"type": "number"})

    assert isinstance(column.type, sqlalchemy.Float)


@pytest.mark.column
def test_number_float():
    """
    GIVEN schema with number type and float format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    column = column_factory.column_factory(spec={"type": "number", "format": "float"})

    assert isinstance(column.type, sqlalchemy.Float)


@pytest.mark.column
def test_number_double():
    """
    GIVEN schema with number type and double format
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory.column_factory(spec={"type": "number", "format": "double"})


@pytest.mark.column
def test_number_unsupported_format():
    """
    GIVEN schema with number type and format that has not been implemented
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory.column_factory(spec={"type": "number", "format": "unsupported"})


@pytest.mark.column
def test_integer():
    """
    GIVEN schema with integer type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    column = column_factory.column_factory(spec={"type": "integer"})

    assert isinstance(column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_integer_int32():
    """
    GIVEN schema with integer type and int32 format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    column = column_factory.column_factory(spec={"type": "integer", "format": "int32"})

    assert isinstance(column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_integer_int64():
    """
    GIVEN schema with integer type and int64 format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy BigInteger column is returned.
    """
    column = column_factory.column_factory(spec={"type": "integer", "format": "int64"})

    assert isinstance(column.type, sqlalchemy.BigInteger)


@pytest.mark.column
def test_integer_unsupported_format():
    """
    GIVEN schema with integer type and unsupported format
    WHEN column_factory is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column_factory.column_factory(spec={"type": "integer", "format": "unsupported"})


@pytest.mark.column
def test_string():
    """
    GIVEN schema with string type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy String column is returned.
    """
    column = column_factory.column_factory(spec={"type": "string"})

    assert isinstance(column.type, sqlalchemy.String)


@pytest.mark.column
def test_string_length():
    """
    GIVEN schema with string type and maxLength property
    WHEN column_factory is called with the schema
    THEN SQLAlchemy String column is returned with the length set to the maxLength.
    """
    column = column_factory.column_factory(spec={"type": "string", "maxLength": 1})

    assert column.type.length == 1


@pytest.mark.column
def test_boolean():
    """
    GIVEN schema with boolean type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy boolean column is returned.
    """
    column = column_factory.column_factory(spec={"type": "boolean"})

    assert isinstance(column.type, sqlalchemy.Boolean)


@pytest.mark.column
def test_handle_object():
    """
    GIVEN
    WHEN _handle_object is called
    THEN the function should exist.
    """
    assert hasattr(column_factory, "_handle_object")


@pytest.mark.column
def test_handle_object_no_tablename():
    """
    GIVEN object schema without x-tablename key
    WHEN _handle_object is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object(spec={"properties": {"id": {}}}, schemas={})


@pytest.mark.column
def test_handle_object_no_properties():
    """
    GIVEN object schema without properties key
    WHEN _handle_object is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object(spec={"x-tablename": "table 1"}, schemas={})


@pytest.mark.column
def test_handle_object_id_missing():
    """
    GIVEN object schema without id in properties
    WHEN _handle_object is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object(
            spec={"x-tablename": "table 1", "properties": {}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_id_no_type():
    """
    GIVEN object schema with id but no type for id
    WHEN _handle_object is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory._handle_object(
            spec={"x-tablename": "table 1", "properties": {"id": {}}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_return():
    """
    GIVEN object schema with x-tablename and id property with a type
    WHEN _handle_object is called with the schema
    THEN a schema with the type of the id property and x-foreign-key property.
    """
    spec = {"x-tablename": "table 1", "properties": {"id": {"type": "idType"}}}
    schemas = {}

    return_value = column_factory._handle_object(spec=spec, schemas=schemas)

    assert return_value == {"type": "idType", "x-foreign-key": "table 1.id"}


@pytest.mark.column
def test_handle_object_ref_return():
    """
    GIVEN object schema with x-tablename and id property that is a $ref
    WHEN _handle_object is called with the schema
    THEN a schema with the type of the id property and x-foreign-key property.
    """
    spec = {
        "x-tablename": "table 1",
        "properties": {"id": {"$ref": "#/components/schemas/IdSchema"}},
    }
    schemas = {"IdSchema": {"type": "idType"}}

    return_value = column_factory._handle_object(spec=spec, schemas=schemas)

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
    [
        (logical_name, column)
    ] = column_factory.column_factory(  # pylint: disable=unexpected-keyword-arg
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
    [
        (fk_logical_name, fk_column),
        (tbl_logical_name, relationship),
    ] = column_factory.column_factory(  # pylint: disable=unexpected-keyword-arg
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"


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
    [
        (logical_name, column)
    ] = column_factory.column_factory(  # pylint: disable=unexpected-keyword-arg
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, sqlalchemy.Boolean)
