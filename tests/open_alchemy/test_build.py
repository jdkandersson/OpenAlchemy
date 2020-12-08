"""Tests for the package builder."""

import pytest

from open_alchemy import build
from open_alchemy import exceptions
from open_alchemy import helpers


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


@pytest.mark.parametrize(
    "schemas, version, title, description, expected_spec_str",
    [
        pytest.param(
            {"Schema1": {}},
            "version 1",
            None,
            None,
            '{"info":{"version":"version 1"},"components":{"schemas":{"Schema1":{}}}}',
            id="no title description",
        ),
        pytest.param(
            {"Schema2": {}},
            "version 2",
            None,
            None,
            '{"info":{"version":"version 2"},"components":{"schemas":{"Schema2":{}}}}',
            id="no title description different schema",
        ),
        pytest.param(
            {},
            "v1",
            "title 1",
            None,
            '{"info":{"version":"v1","title":"title 1"},"components":{"schemas":{}}}',
            id="with title",
        ),
        pytest.param(
            {},
            "v1",
            None,
            "d1",
            '{"info":{"version":"v1","description":"d1"},"components":{"schemas":{}}}',
            id="with description",
        ),
    ],
)
@pytest.mark.build
def test_generate_spec_str(schemas, version, title, description, expected_spec_str):
    """
    GIVEN schemas, version, title and description
    WHEN generate_spec_str is called with the schemas, version, title and description
    THEN the spected spec string is returned.
    """
    returned_spec_str = build.generate_spec_str(
        schemas=schemas, version=version, title=title, description=description
    )

    assert returned_spec_str == expected_spec_str


@pytest.mark.build
def test_calculate_spec_info_version():
    """
    GIVEN spec
    WHEN calculate_spec_info is called with the spec
    THEN the version is returned.
    """
    spec = {}
    schemas = {}

    spec_info = build.calculate_spec_info(spec=spec, schemas=schemas)

    assert spec_info.version == "63581fa2bdc5cef14183"


@pytest.mark.build
def test_calculate_spec_info_spec_str():
    """
    GIVEN spec
    WHEN calculate_spec_info is called with the spec
    THEN the string representation of it is returned.
    """
    spec = {}
    schemas = {}

    spec_info = build.calculate_spec_info(spec=spec, schemas=schemas)

    assert (
        spec_info.spec_str
        == '{"info":{"version":"63581fa2bdc5cef14183"},"components":{"schemas":{}}}'
    )


@pytest.mark.parametrize(
    "info, expected_title",
    [
        pytest.param({}, None, id="not defined"),
        pytest.param({"title": "title 1"}, "title 1", id="defined"),
        pytest.param({"title": "title 2"}, "title 2", id="defined different"),
    ],
)
@pytest.mark.build
def test_calculate_spec_info_title(info, expected_title):
    """
    GIVEN info and spec
    WHEN calculate_spec_info is called with the spec
    THEN the title is returned.
    """
    spec = {"info": info}
    schemas = {}

    spec_info = build.calculate_spec_info(spec=spec, schemas=schemas)

    assert spec_info.title == expected_title
    if expected_title is not None:
        assert expected_title in spec_info.spec_str


@pytest.mark.parametrize(
    "info, expected_description",
    [
        pytest.param({}, None, id="not defined"),
        pytest.param({"description": "description 1"}, "description 1", id="defined"),
        pytest.param(
            {"description": "description 2"}, "description 2", id="defined different"
        ),
    ],
)
@pytest.mark.build
def test_calculate_spec_info_description(info, expected_description):
    """
    GIVEN info and spec
    WHEN calculate_spec_info is called with the spec
    THEN the description is returned.
    """
    spec = {"info": info}
    schemas = {}

    spec_info = build.calculate_spec_info(spec=spec, schemas=schemas)

    assert spec_info.description == expected_description
    if expected_description is not None:
        assert expected_description in spec_info.spec_str


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


@pytest.mark.build
def test_dump(tmp_path):
    """
    GIVEN path
    WHEN dump is called with the path
    THEN the expected directory structure is returned.
    """
    dist_path = tmp_path / "dist"
    dist_path.mkdir()

    name = "name 1"
    setup = "setup file"
    manifest = "manifest file"
    spec_str = "spec file"
    init = "init file"

    build.dump(
        path=str(dist_path),
        name=name,
        setup=setup,
        manifest=manifest,
        spec_str=spec_str,
        init=init,
    )

    # Define generated project directories
    project_path = dist_path / name
    package_path = project_path / name

    # Check setup file
    expected_setup_path = project_path / "setup.py"
    assert expected_setup_path.is_file()
    with open(expected_setup_path) as in_file:
        assert in_file.read() == setup

    # Check manifest file
    expected_manifest_path = project_path / "MANIFEST.in"
    assert expected_manifest_path.is_file()
    with open(expected_manifest_path) as in_file:
        assert in_file.read() == manifest

    # Check spec file
    expected_spec_path = package_path / "spec.json"
    assert expected_spec_path.is_file()
    with open(expected_spec_path) as in_file:
        assert in_file.read() == spec_str

    # Check init file
    expected_init_path = package_path / "__init__.py"
    assert expected_init_path.is_file()
    with open(expected_init_path) as in_file:
        assert in_file.read() == init


@pytest.mark.build
def test_dump_path_not_exists(tmp_path):
    """
    GIVEN path that doesn't exist
    WHEN dump is called with the path
    THEN no exceptions are raised.
    """
    dist_path = tmp_path / "dist"

    name = "name 1"
    setup = "setup file"
    manifest = "manifest file"
    spec_str = "spec file"
    init = "init file"

    build.dump(
        path=str(dist_path),
        name=name,
        setup=setup,
        manifest=manifest,
        spec_str=spec_str,
        init=init,
    )


@pytest.mark.build
def test_dump_path_is_file(tmp_path):
    """
    GIVEN path that is a file
    WHEN dump is called with the path
    THEN BuildError is raised.
    """
    dist_path = tmp_path / "dist"
    with open(dist_path, "w") as out_file:
        out_file.write("")

    name = "name 1"
    setup = "setup file"
    manifest = "manifest file"
    spec_str = "spec file"
    init = "init file"

    with pytest.raises(exceptions.BuildError):
        build.dump(
            path=str(dist_path),
            name=name,
            setup=setup,
            manifest=manifest,
            spec_str=spec_str,
            init=init,
        )


@pytest.mark.build
def test_dump_path_name_exists(tmp_path):
    """
    GIVEN path and name that does exist
    WHEN dump is called with the path
    THEN no exceptions are raised.
    """
    dist_path = tmp_path / "dist"
    dist_path.mkdir()

    name = "name 1"
    setup = "setup file"
    manifest = "manifest file"
    spec_str = "spec file"
    init = "init file"

    (dist_path / name).mkdir()

    build.dump(
        path=str(dist_path),
        name=name,
        setup=setup,
        manifest=manifest,
        spec_str=spec_str,
        init=init,
    )


@pytest.mark.build
def test_dump_path_name_is_file(tmp_path):
    """
    GIVEN path and name that points to a file
    WHEN dump is called with the path
    THEN BuildError is raised.
    """
    dist_path = tmp_path / "dist"
    dist_path.mkdir()

    name = "name 1"
    setup = "setup file"
    manifest = "manifest file"
    spec_str = "spec file"
    init = "init file"

    with open(dist_path / name, "w") as out_file:
        out_file.write("")

    with pytest.raises(exceptions.BuildError):
        build.dump(
            path=str(dist_path),
            name=name,
            setup=setup,
            manifest=manifest,
            spec_str=spec_str,
            init=init,
        )


@pytest.mark.parametrize(
    "spec, schemas, expected_version",
    [
        pytest.param(
            True, {"key": "value 1"}, "8a9545946e69e534df1d", id="spec not dict"
        ),
        pytest.param(
            True,
            {"key": "value 2"},
            "e44d6e49a1b667e4b9bf",
            id="spec not dict schemas different",
        ),
        pytest.param(
            {}, {"key": "value 1"}, "8a9545946e69e534df1d", id="spec info missing"
        ),
        pytest.param(
            {"info": True},
            {"key": "value 1"},
            "8a9545946e69e534df1d",
            id="spec info not dict",
        ),
        pytest.param(
            {"info": {}},
            {"key": "value 1"},
            "8a9545946e69e534df1d",
            id="spec info version missing",
        ),
        pytest.param(
            {"info": {"version": True}},
            {"key": "value 1"},
            "8a9545946e69e534df1d",
            id="spec info version not string",
        ),
        pytest.param(
            {"info": {"version": "version 1"}},
            {"key": "value 1"},
            "version 1",
            id="spec info version string",
        ),
    ],
)
@pytest.mark.build
def test_calculate_version(spec, schemas, expected_version):
    """
    GIVEN spec and schemas
    WHEN calculate_version is called with the spec and schemas
    THEN the expected version is returned.
    """
    returned_version = build.calculate_version(spec=spec, schemas=schemas)

    assert returned_version == expected_version


@pytest.mark.parametrize(
    "package_format, extensions",
    [
        pytest.param(build.PackageFormat.NONE, [], id="build without package"),
        pytest.param(
            build.PackageFormat.SDIST, [".tar.gz"], id="build with a sdist package"
        ),
        pytest.param(
            build.PackageFormat.WHEEL,
            [".whl"],
            id="build with a wheel package",
        ),
        pytest.param(
            build.PackageFormat.SDIST | build.PackageFormat.WHEEL,
            [".tar.gz", "whl"],
            id="build with all available packages",
        ),
    ],
)
@pytest.mark.build
def test_execute(tmp_path, package_format, extensions):
    """
    GIVEN spec, name, path and a package format
    WHEN execute is called with the spec, name and path
    THEN the setup.py, MANIFEST.in, spec.json and __init__.py files are created.
    """
    dist = tmp_path / "dist"
    dist.mkdir()

    name = "app_models"
    version = "version 1"
    spec = {
        "info": {
            "version": version,
        },
        "components": {
            "schemas": {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        },
    }

    build.execute(spec=spec, name=name, path=str(dist), format_=package_format)

    # Define generated project directories
    project_path = dist / name
    package_path = project_path / name

    # Check setup file
    expected_setup_path = project_path / "setup.py"
    assert expected_setup_path.is_file()
    with open(expected_setup_path) as in_file:
        setup_file_contents = in_file.read()
        assert name in setup_file_contents
        assert version in setup_file_contents

    # Check manifest file
    expected_manifest_path = project_path / "MANIFEST.in"
    assert expected_manifest_path.is_file()
    with open(expected_manifest_path) as in_file:
        manifest_file_contents = in_file.read()
        assert name in manifest_file_contents

    # Check spec file
    expected_spec_path = package_path / "spec.json"
    assert expected_spec_path.is_file()
    with open(expected_spec_path) as in_file:
        spec_file_contents = in_file.read()
        assert version in spec_file_contents
        assert "Schema" in spec_file_contents
        assert "x-tablename" in spec_file_contents

    # Check init file
    expected_init_path = package_path / "__init__.py"
    assert expected_init_path.is_file()
    with open(expected_init_path) as in_file:
        init_contents = in_file.read()
    assert (
        """import pathlib

from open_alchemy import init_json

parent_path = pathlib.Path(__file__).parent.absolute()
init_json(parent_path / "spec.json")"""
        in init_contents
    )
    assert "class SchemaDict" in init_contents
    assert "id: typing.Optional[int]" in init_contents
    assert "class TSchema" in init_contents
    assert "id: 'sqlalchemy.Column[typing.Optional[int]]'" in init_contents
    assert "Schema: typing.Type[TSchema]" in init_contents

    # Assert one package per requested format is created.
    for extension in extensions:
        dist_dir = project_path / "dist"
        files = list(dist_dir.glob(f"{name}*{extension}"))
        assert len(files) == 1


@pytest.mark.integration
def test_build_dist_wheel_import_error(tmp_path):
    """
    GIVEN wheel package is not available
    WHEN build_dist is called
    THEN RuntimeError is raised.
    """
    dist = tmp_path / "dist"
    dist.mkdir()

    name = "app_models"
    version = "version 1"
    spec = {
        "info": {
            "version": version,
        },
        "components": {
            "schemas": {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        },
    }

    try:
        helpers.command.run(["pip", "uninstall", "-y", "wheel"], ".")
        with pytest.raises(RuntimeError):
            build.execute(
                spec=spec, name=name, path=str(dist), format_=build.PackageFormat.WHEEL
            )
    finally:
        helpers.command.run(["pip", "install", "wheel"], ".")


@pytest.mark.parametrize(
    "format_",
    [
        pytest.param(build.PackageFormat.NONE, id="build no archive"),
        pytest.param(build.PackageFormat.SDIST, id="build a sdist archive"),
        pytest.param(build.PackageFormat.WHEEL, id="build a wheel archive"),
        pytest.param(
            build.PackageFormat.SDIST | build.PackageFormat.WHEEL,
            id="build a sdist and a wheel archive",
        ),
    ],
)
@pytest.mark.build
def test_validate_dist_format_valid(format_):
    """
    GIVEN a valid format
    WHEN validate_dist_format is called
    THEN nothing happens
    """
    build.validate_dist_format(format_)


@pytest.mark.build
def test_validate_dist_format_invalid():
    """
    GIVEN a invalid format
    WHEN validate_dist_format is called
    THEN an exception is raised
    """
    with pytest.raises(exceptions.BuildError):
        format_ = build.PackageFormat.NONE | build.PackageFormat.SDIST
        build.validate_dist_format(format_)
