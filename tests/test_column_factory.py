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
def test_type_not_implemented():
    """
    GIVEN column schema with type that has not been implemented
    WHEN column_factory is called with the schema
    THEN NotImplementedError is raised.
    """
    with pytest.raises(NotImplementedError):
        column_factory.column_factory(schema={"type": "not_implemented"})


@pytest.mark.column
def test_column_return():
    """
    GIVEN valid schema
    WHEN column_factory is called with the schema
    THEN an instance of SQLAlchemy Column is returned.
    """
    column = column_factory.column_factory(schema={"type": "number"})

    assert isinstance(column, sqlalchemy.Column)


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
    WHEN column factory is called with the schema
    THEN SQLAlchemy float column is returned.
    """
    column = column_factory.column_factory(schema={"type": "number"})

    assert isinstance(column.type, sqlalchemy.Float)
