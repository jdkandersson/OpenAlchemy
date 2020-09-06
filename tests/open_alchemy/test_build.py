"""Tests for the package builder."""

import pytest

from open_alchemy import build
from open_alchemy import exceptions


@pytest.mark.parametrize(
    "spec",
    [
        pytest.param(True, id="base invalid"),
        pytest.param({"components": {"schemas": {}}}, id="no schemas"),
        pytest.param(
            {
                "components": {
                    "schemas": {
                        "Schema1": {
                            "x-tablename": "schema_1",
                        }
                    }
                }
            },
            id="schema invalid",
        ),
    ],
)
@pytest.mark.build
def test_get_schemas_invalid(spec):
    """
    GIVEN invalid spec
    WHEN get_schemas is called
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        build.get_schemas(spec=spec)


@pytest.mark.build
def test_get_schemas_valid():
    """
    GIVEN invalid spec
    WHEN get_schemas is called
    THEN MalformedSchemaError is raised.
    """
    spec = {
        "components": {
            "schemas": {
                "Schema1": {
                    "type": "object",
                    "x-tablename": "schema_1",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        }
    }

    returned_schemas = build.get_schemas(spec=spec)

    assert returned_schemas == {
        "Schema1": {
            "type": "object",
            "x-tablename": "schema_1",
            "properties": {"id": {"type": "integer"}},
        }
    }


@pytest.mark.build
def test_generate_spec():
    """
    GIVEN schemas
    WHEN generate_spec is called with the schemas
    THEN the spec.json file contents with the schemas are returned.
    """
    schemas = {
        "Schema1": {
            "type": "object",
            "x-tablename": "schema_1",
            "properties": {"id": {"type": "integer"}},
        }
    }

    returned_contents = build.generate_spec(schemas=schemas)

    expected_contents = (
        '{"components":{"schemas":{"Schema1":'
        '{"type":"object","x-tablename":"schema_1",'
        '"properties":{"id":{"type":"integer"}}}}}}'
    )

    assert returned_contents == expected_contents


@pytest.mark.build
def test_generate_setup():
    """
    GIVEN name and version
    WHEN generate_setup is called with the name and version
    THEN the setup.py file contents with the name and version are returned.
    """
    name = "name 1"
    version = "version 1"

    returned_contents = build.generate_setup(name=name, version=version)

    expected_contents = """import setuptools

setuptools.setup(
    name="name 1",
    version="version 1",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "OpenAlchemy",
    ],
    include_package_data=True,
)
"""

    assert returned_contents == expected_contents


@pytest.mark.build
def test_generate_manifest():
    """
    GIVEN name
    WHEN generate_manifest is called with the name
    THEN the MAINFEST.in file contents with the name are returned.
    """
    name = "name 1"

    returned_contents = build.generate_manifest(name=name)

    expected_contents = """recursive-include name 1 *.json
remove .*
"""

    assert returned_contents == expected_contents


@pytest.mark.build
def test_generate_init_open_alchemy():
    """
    GIVEN name and version
    WHEN generate_init_open_alchemy is called with the name and version
    THEN the __init__.py file contents with the name and version are returned.
    """
    returned_contents = build.generate_init_open_alchemy()

    expected_contents = """import pathlib

from open_alchemy import init_json

parent_path = pathlib.Path(__file__).parent.absolute()
init_json(parent_path / "spec.json")"""

    assert returned_contents == expected_contents


GENERATE_INIT_MODELS_FILE_TESTS = [
    # pylint: disable=line-too-long
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (
            "class Schema1Dict",
            "id: typing.Optional[int]",
            "class TSchema1",
            "id: 'sqlalchemy.Column[typing.Optional[int]]'",
            "Schema1: typing.Type[TSchema1]",
        ),
        id="single",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {
                        "type": "object",
                        "x-tablename": "schema_1",
                        "properties": {"id": {"type": "integer"}},
                        "x-inherits": True,
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            "ParentSchema": {
                "type": "object",
                "x-tablename": "parent_schema",
                "properties": {"parent_id": {"type": "integer"}},
            },
        },
        (
            "class Schema1Dict",
            "id: typing.Optional[int]",
            "parent_id: typing.Optional[int]",
            "class TSchema1",
            "id: 'sqlalchemy.Column[typing.Optional[int]]'",
            "parent_id: 'sqlalchemy.Column[typing.Optional[int]]'",
            "Schema1: typing.Type[TSchema1]",
            "class ParentSchemaDict",
            "parent_id: typing.Optional[int]",
            "class TParentSchema",
            "parent_id: 'sqlalchemy.Column[typing.Optional[int]]'",
            "ParentSchema: typing.Type[TParentSchema] = models.ParentSchema",
        ),
        id="inherits",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {
                    "id": {"type": "integer"},
                    "schema_2": {
                        "allOf": [
                            {"$ref": "#/components/schemas/Schema2"},
                            {"x-backref": "schema_1"},
                        ]
                    },
                },
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"id": {"type": "integer"}},
            },
        },
        (
            "class Schema1Dict",
            "id: typing.Optional[int]",
            'schema_2: typing.Optional["Schema2Dict"]',
            "class TSchema1",
            "id: 'sqlalchemy.Column[typing.Optional[int]]'",
            "schema_2: 'sqlalchemy.Column[typing.Optional[\"TSchema2\"]]'",
            "Schema1: typing.Type[TSchema1]",
            "class Schema2Dict",
            "id: typing.Optional[int]",
            "class TSchema2",
            "id: 'sqlalchemy.Column[typing.Optional[int]]'",
            "schema_1: 'sqlalchemy.Column[typing.Sequence[\"TSchema1\"]]'",
            "Schema2: typing.Type[TSchema2] = models.Schema2",
        ),
        id="backref",
    ),
]


@pytest.mark.parametrize("schemas, expected_contents", GENERATE_INIT_MODELS_FILE_TESTS)
@pytest.mark.build
def test_generate_init_models_file(schemas, expected_contents):
    """
    GIVEN schemas and expected contents
    WHEN generate_init_models_file is called with the schemas
    THEN the expected __init__.py file contents are returned.
    """
    returned_contents = build.generate_init_models_file(schemas=schemas)

    for expected_content in expected_contents:
        assert expected_content in returned_contents


@pytest.mark.build
def test_generate_init():
    """
    GIVEN open alchemy and models file contents
    WHEN generate_init is called with the open alchemy and models file contents
    THEN the __init__.py file contents with the open alchemy and models file contents
        are returned.
    """
    returned_contents = build.generate_init(
        open_alchemy="open alchemy", models_file="models file"
    )

    expected_contents = """open alchemy


models file"""

    assert returned_contents == expected_contents
