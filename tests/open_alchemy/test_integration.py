"""Integration tests."""

import json
import typing
from unittest import mock

import pytest
import sqlalchemy
import yaml
from sqlalchemy.ext import declarative

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


@pytest.mark.prod_env
@pytest.mark.integration
def test_empty_spec():
    """
    GIVEN empty specification
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(open_alchemy.exceptions.MalformedSpecificationError):
        open_alchemy.init_model_factory(base=None, spec={})


@pytest.mark.prod_env
@pytest.mark.integration
def test_empty_components():
    """
    GIVEN specification with empty components
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(open_alchemy.exceptions.MalformedSpecificationError):
        open_alchemy.init_model_factory(base=None, spec={"components": {}})


@pytest.mark.prod_env
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


@pytest.mark.prod_env
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


@pytest.mark.prod_env
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


@pytest.mark.prod_env
@pytest.mark.parametrize(
    "type_, format_, value",
    [
        ("integer", None, 1),
        ("integer", "int64", 1),
        ("number", None, 1.0),
        ("string", None, "some string"),
        ("boolean", None, True),
    ],
)
@pytest.mark.integration
def test_database_types(
    engine, sessionmaker, type_: str, format_: typing.Optional[str], value: typing.Any
):
    """
    GIVEN specification with a schema with a given type column and a value for that
        column
    WHEN schema is created and an instance is added to the session
    THEN the instance is returned when the session is queried for it.
    """
    # Defining specification
    column_schema = {"type": type_, "x-primary-key": True}
    if format_ is not None:
        column_schema["format"] = format_
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {"column": column_schema},
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.prod_env
@pytest.mark.parametrize("index", ["x-primary-key", "x-index", "x-unique"])
@pytest.mark.integration
def test_database_indexes(engine, index: str):
    """
    GIVEN specification with a schema with an integer and given index
    WHEN schema is created
    THEN no exceptions get raised.
    """
    # Defining specification
    column_schema = {"type": "integer", index: True}
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "column": column_schema,
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)


@pytest.mark.prod_env
@pytest.mark.integration
def test_database_autoincrement(engine, sessionmaker):
    """
    GIVEN specification with a schema with an autoincrement id column
    WHEN schema is created, values inserted without id column
    THEN the data is returned as it was inserted with autogenerated value.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": True,
                        },
                        "name": {"type": "string"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    model_instance = model(name="table name 1")
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 1
    assert queried_model.name == "table name 1"


@pytest.mark.prod_env
@pytest.mark.integration
def test_database_not_autoincrement(engine, sessionmaker):
    """
    GIVEN specification with a schema with autoincrement disabled id column
    WHEN schema is created, values inserted without id column
    THEN exception is raised.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": False,
                        },
                        "name": {"type": "string"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    model_instance = model(name="table name 1")
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.orm.exc.FlushError):
        session.flush()


@pytest.mark.prod_env
@pytest.mark.integration
def test_database_many_to_one_relationship(engine, sessionmaker):
    """
    GIVEN specification with a schema with an object relationship
    WHEN schema is created, values inserted in both tables and queried
    THEN the data is returned as it was inserted.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "RefTable": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                    },
                    "x-tablename": "ref_table",
                    "x-backref": "tables",
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_table": {"$ref": "#/components/schemas/RefTable"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")
    ref_model = model_factory(name="RefTable")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    ref_model_instance = ref_model(id=11, name="ref table name 1")
    model_instance = model(id=12, name="table name 1", ref_table=ref_model_instance)
    session = sessionmaker()
    session.add(ref_model_instance)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 12
    assert queried_model.name == "table name 1"
    assert queried_model.ref_table_id == 11
    assert queried_model.ref_table.id == 11
    assert queried_model.ref_table.name == "ref table name 1"
    queried_ref_model = session.query(ref_model).first()
    assert queried_ref_model.id == 11
    assert queried_ref_model.name == "ref table name 1"
    assert len(queried_ref_model.tables) == 1
    assert queried_ref_model.tables[0].id == 12


@pytest.mark.parametrize(
    "spec",
    [
        {
            "components": {
                "schemas": {
                    "Column": {"type": "integer", "x-primary-key": True},
                    "Table": {
                        "properties": {
                            "column": {"$ref": "#/components/schemas/Column"}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
        {
            "components": {
                "schemas": {
                    "Table": {"$ref": "#/components/schemas/RefTable"},
                    "RefTable": {
                        "properties": {
                            "column": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
        {
            "components": {
                "schemas": {
                    "Table": {
                        "properties": {
                            "column": {
                                "allOf": [{"type": "integer", "x-primary-key": True}]
                            }
                        },
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
        {
            "components": {
                "schemas": {
                    "Table": {
                        "allOf": [
                            {
                                "properties": {
                                    "column": {"type": "integer", "x-primary-key": True}
                                },
                                "x-tablename": "table",
                                "type": "object",
                            }
                        ]
                    }
                }
            }
        },
    ],
    ids=["ref column", "ref model", "allOf column", "allOf model"],
)
@pytest.mark.integration
def test_database_feature(engine, sessionmaker, spec):
    """
    GIVEN specification with a schema that has a $ref on a column
    WHEN schema is created and an instance is added to the session
    THEN the instance is returned when the session is queried for it.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(column=1)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == 1


BASIC_SPEC = {
    "components": {
        "schemas": {
            "Table": {
                "properties": {"column": {"type": "integer", "x-primary-key": True}},
                "x-tablename": "table",
                "type": "object",
            }
        }
    }
}


@pytest.mark.integration
def test_init_json(engine, sessionmaker, tmp_path):
    """
    GIVEN specification stored in a JSON file
    WHEN init_json is called with the file
    THEN a valid model factory is returned.
    """
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.json"
    spec_file.write_text(json.dumps(BASIC_SPEC))

    # Creating model factory
    base, model_factory = open_alchemy.init_json(str(spec_file), define_all=False)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    value = 0
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_init_yaml(engine, sessionmaker, tmp_path):
    """
    GIVEN specification stored in a YAML file
    WHEN init_yaml is called with the file
    THEN a valid model factory is returned.
    """
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Creating model factory
    base, model_factory = open_alchemy.init_yaml(str(spec_file), define_all=False)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    value = 0
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_init_yaml_import_error():
    """
    GIVEN yaml package is not available
    WHEN init_yaml is called
    THEN ImportError is raised.
    """
    with mock.patch.dict("sys.modules", {"yaml": None}):
        with pytest.raises(ImportError):
            open_alchemy.init_yaml("some file")


@pytest.mark.integration
def test_import_base_initial():
    """
    GIVEN
    WHEN
    THEN ImportError is raised when Base is imported from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel,unused-import
    with pytest.raises(ImportError):
        from open_alchemy.models import Base  # noqa: F401


@pytest.mark.integration
def test_import_base(tmp_path):
    """
    GIVEN specification file
    WHEN init_yaml is called with the specification file
    THEN Base can be imported from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel,unused-import
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Creating model factory
    open_alchemy.init_yaml(str(spec_file))

    from open_alchemy.models import Base  # noqa: F401


@pytest.mark.integration
def test_import_model(engine, sessionmaker, tmp_path):
    """
    GIVEN specification stored in a YAML file
    WHEN init_yaml is called with the file
    THEN the model is importable from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Creating model factory
    open_alchemy.init_yaml(str(spec_file), define_all=True)

    # Creating models
    from open_alchemy.models import Base

    Base.metadata.create_all(engine)

    # Creating model instance
    from open_alchemy.models import Table

    value = 0
    model_instance = Table(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(Table).first()
    assert queried_model.column == value
