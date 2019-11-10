"""Integration tests for initialization."""

from unittest import mock

import pytest
import sqlalchemy

import open_alchemy


@pytest.mark.integration
def test_init_optional_base_none_call(
    mocked_init_model_factory: mock.MagicMock, mocked_declarative_base: mock.MagicMock
):
    """
    GIVEN mocked init_model_factory and declarative_base
    WHEN _init_optional_base is called with none base
    THEN init_model_factory is called with declarative_base return value as base.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()

    open_alchemy._init_optional_base(base=None, spec=spec, define_all=True)

    mocked_init_model_factory.assert_called_once_with(
        base=mocked_declarative_base.return_value, spec=spec, define_all=True
    )


@pytest.mark.integration
def test_init_optional_base_none_return(
    _mocked_init_model_factory: mock.MagicMock, mocked_declarative_base: mock.MagicMock
):
    """
    GIVEN mocked init_model_factory and declarative_base
    WHEN _init_optional_base is called with none base
    THEN the declarative_base return value is returned as base.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()

    base, _ = open_alchemy._init_optional_base(base=None, spec=spec, define_all=True)

    assert base == mocked_declarative_base.return_value


@pytest.mark.integration
def test_init_optional_base_def_call(mocked_init_model_factory: mock.MagicMock):
    """
    GIVEN mocked init_model_factory and mock base
    WHEN _init_optional_base is called with the base
    THEN init_model_factory is called with base.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()
    base = mock.MagicMock()

    open_alchemy._init_optional_base(base=base, spec=spec, define_all=True)

    mocked_init_model_factory.assert_called_once_with(
        base=base, spec=spec, define_all=True
    )


@pytest.mark.integration
def test_init_optional_base_def_return(_mocked_init_model_factory: mock.MagicMock):
    """
    GIVEN mocked init_model_factory and and mock base
    WHEN _init_optional_base is called with the base
    THEN the base is returned.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()
    base = mock.MagicMock()

    returned_base, _ = open_alchemy._init_optional_base(
        base=base, spec=spec, define_all=True
    )

    assert returned_base == base


@pytest.mark.integration
def test_empty_spec():
    """
    GIVEN empty specification
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(open_alchemy.exceptions.MalformedSpecificationError):
        open_alchemy.init_model_factory(base=None, spec={})


@pytest.mark.integration
def test_empty_components():
    """
    GIVEN specification with empty components
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(open_alchemy.exceptions.MalformedSpecificationError):
        open_alchemy.init_model_factory(base=None, spec={"components": {}})


@pytest.mark.integration
def test_cache_diff(mocked_model_factory: mock.MagicMock):
    """
    GIVEN valid specification and mocked model_factory
    WHEN return value of init_model_factory is called with different names
    THEN mocked model_factory is called the same number of times the return value is
        called.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock, spec={"components": {"schemas": {}}}
    )

    model_factory(name="table 1")
    model_factory(name="table 2")

    assert mocked_model_factory.call_count == 2


@pytest.mark.integration
def test_cache_same(mocked_model_factory: mock.MagicMock):
    """
    GIVEN valid specification and mocked model_factory
    WHEN return value of init_model_factory is called multiple times with the same name
    THEN mocked model_factory is called once.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock, spec={"components": {"schemas": {}}}
    )

    model_factory(name="table 1")
    model_factory(name="table 1")

    assert mocked_model_factory.call_count == 1


@pytest.mark.integration
def test_schema():
    """
    GIVEN valid specification with single property
    WHEN return value of init_model_factory is called with the name of the schema
    THEN a SQLAlchemy model with a single property is returned.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "Table": {
                        "properties": {"column": {"type": "integer"}},
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
    )

    model = model_factory(name="Table")

    # Checking model
    assert model.__tablename__ == "table"
    assert hasattr(model, "column")
    assert isinstance(model.column.type, sqlalchemy.Integer)
