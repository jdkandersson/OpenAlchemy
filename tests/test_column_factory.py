"""Tests for the column factory."""

import pytest
import sqlalchemy

from openapi_sqlalchemy import column_factory


@pytest.mark.column
def test_type_missing():
    """
    GIVEN column schema that does not have the type key
    WHEN column_factory is called with the schema
    THEN TypeError is raised.
    """
    with pytest.raises(TypeError):
        column_factory.column_factory(schema={})


@pytest.mark.column
def test_type_unsupported():
    """
    GIVEN column schema with type that has not been implemented
    WHEN column_factory is called with the schema
    THEN NotImplementedError is raised.
    """
    with pytest.raises(NotImplementedError):
        column_factory.column_factory(schema={"type": "unsupported"})


@pytest.mark.column
def test_column_return():
    """
    GIVEN valid schema
    WHEN column_factory is called with the schema
    THEN an instance of SQLAlchemy Column is returned.
    """
    column = column_factory.column_factory(schema={"type": "number"})

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
        schema={"type": "number", "x-primary-key": primary_key}
    )

    assert column.primary_key == primary_key


@pytest.mark.column
def test_required():
    """
    GIVEN valid schema
    WHEN column_factory is called with the schema and required set
    THEN SQLAlchemy column is returned that is nullable reset.
    """
    column = column_factory.column_factory(schema={"type": "number"}, required=True)

    assert not column.nullable


@pytest.mark.column
def test_number():
    """
    GIVEN schema with number type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    column = column_factory.column_factory(schema={"type": "number"})

    assert isinstance(column.type, sqlalchemy.Float)


@pytest.mark.column
def test_integer():
    """
    GIVEN schema with integer type
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    column = column_factory.column_factory(schema={"type": "integer"})

    assert isinstance(column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_integer_int32():
    """
    GIVEN schema with integer type and int32 format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    column = column_factory.column_factory(
        schema={"type": "integer", "format": "int32"}
    )

    assert isinstance(column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_integer_int64():
    """
    GIVEN schema with integer type and int64 format
    WHEN column_factory is called with the schema
    THEN SQLAlchemy BigInteger column is returned.
    """
    column = column_factory.column_factory(
        schema={"type": "integer", "format": "int64"}
    )

    assert isinstance(column.type, sqlalchemy.BigInteger)


@pytest.mark.column
def test_integer_unsupported_format():
    """
    GIVEN schema with integer type and unsupported format
    WHEN column_factory is called with the schema
    THEN NotImplementedError is raised.
    """
    with pytest.raises(NotImplementedError):
        column_factory.column_factory(
            schema={"type": "integer", "format": "unsupported"}
        )
