"""Tests for the column factory."""
# pylint: disable=protected-access

import typing

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy.column_factory import column


@pytest.mark.column
def test_spec_to_column_no_type():
    """
    GIVEN column schema without type
    WHEN _spec_to_column is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        column._spec_to_column(spec={})


@pytest.mark.column
def test_spec_to_column_type_unsupported():
    """
    GIVEN column schema with type that has not been implemented
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "unsupported"})


@pytest.mark.column
def test_spec_to_column_column_return():
    """
    GIVEN valid schema
    WHEN _spec_to_column is called with the schema
    THEN an instance of SQLAlchemy Column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "number"})

    assert isinstance(returned_column, sqlalchemy.Column)


@pytest.mark.parametrize("primary_key", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_primary_key(primary_key: bool):
    """
    GIVEN valid schema and the value of the primary key property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column primary_key property is set to the input.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-primary-key": primary_key}
    )

    assert returned_column.primary_key == primary_key


@pytest.mark.parametrize("autoincrement", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_autoincrement(autoincrement: bool):
    """
    GIVEN valid schema and the value of the autoincrement property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column autoincrement property is set to the input.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-autoincrement": autoincrement}
    )

    assert returned_column.autoincrement == autoincrement


@pytest.mark.parametrize("index", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_index(index: bool):
    """
    GIVEN valid schema and the value of the index property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column index property is set to the input.
    """
    returned_column = column._spec_to_column(spec={"type": "number", "x-index": index})

    assert returned_column.index == index


@pytest.mark.parametrize("unique", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_unique(unique: bool):
    """
    GIVEN valid schema and the value of the unique property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column unique property is set to the input.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-unique": unique}
    )

    assert returned_column.unique == unique


@pytest.mark.column
def test_spec_to_column_foreign_key():
    """
    GIVEN valid schema which has x-foreign-key set
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column foreign key property is set.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-foreign-key": "foreign.key"}
    )

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
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
    WHEN _spec_to_column is called with the schema and required argument
    THEN SQLAlchemy column is returned where nullable property is equal to the
        expected input.
    """
    kwargs: typing.Dict[str, bool] = {}
    if required is not None:
        kwargs["required"] = required
    schema: typing.Dict[str, typing.Union[str, bool]] = {"type": "number"}
    if nullable is not None:
        schema["nullable"] = nullable
    returned_column = column._spec_to_column(spec=schema, **kwargs)

    assert returned_column.nullable == expected


@pytest.mark.column
def test_spec_to_column_number():
    """
    GIVEN schema with number type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "number"})

    assert isinstance(returned_column.type, sqlalchemy.Float)


@pytest.mark.column
def test_spec_to_column_number_float():
    """
    GIVEN schema with number type and float format
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "number", "format": "float"})

    assert isinstance(returned_column.type, sqlalchemy.Float)


@pytest.mark.column
def test_spec_to_column_number_double():
    """
    GIVEN schema with number type and double format
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "number", "format": "double"})


@pytest.mark.column
def test_spec_to_column_number_unsupported_format():
    """
    GIVEN schema with number type and format that has not been implemented
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "number", "format": "unsupported"})


@pytest.mark.column
def test_spec_to_column_integer():
    """
    GIVEN schema with integer type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "integer"})

    assert isinstance(returned_column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_spec_to_column_integer_int32():
    """
    GIVEN schema with integer type and int32 format
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    returned_column = column._spec_to_column(
        spec={"type": "integer", "format": "int32"}
    )

    assert isinstance(returned_column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_spec_to_column_integer_int64():
    """
    GIVEN schema with integer type and int64 format
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy BigInteger column is returned.
    """
    returned_column = column._spec_to_column(
        spec={"type": "integer", "format": "int64"}
    )

    assert isinstance(returned_column.type, sqlalchemy.BigInteger)


@pytest.mark.column
def test_spec_to_column_integer_unsupported_format():
    """
    GIVEN schema with integer type and unsupported format
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "integer", "format": "unsupported"})


@pytest.mark.column
def test_spec_to_column_string():
    """
    GIVEN schema with string type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy String column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "string"})

    assert isinstance(returned_column.type, sqlalchemy.String)


@pytest.mark.column
def test_spec_to_column_string_length():
    """
    GIVEN schema with string type and maxLength property
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy String column is returned with the length set to the maxLength.
    """
    returned_column = column._spec_to_column(spec={"type": "string", "maxLength": 1})

    assert returned_column.type.length == 1


@pytest.mark.column
def test_spec_to_column_boolean():
    """
    GIVEN schema with boolean type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy boolean column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "boolean"})

    assert isinstance(returned_column.type, sqlalchemy.Boolean)


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle_column is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    returned_column = column.handle_column(spec={"type": "number"})

    assert isinstance(returned_column, sqlalchemy.Column)
