"""Tests for artifacts."""
# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file

_ColSchemaArtifacts = models_file.types.ColumnSchemaArtifacts
_ColSchemaOAArtifacts = models_file.types.ColumnSchemaOpenAPIArtifacts
_ColSchemaExtArtifacts = models_file.types.ColumnSchemaExtensionArtifacts
_ColumnArtifacts = models_file.types.ColumnArtifacts
_ColumnArgArtifacts = models_file.types.ColumnArgArtifacts


@pytest.mark.parametrize(
    "schema, required, expected_artifacts",
    [
        pytest.param(
            {"type": "type 1"},
            None,
            _ColSchemaArtifacts(open_api=_ColSchemaOAArtifacts(type="type 1")),
            id="type only",
        ),
        pytest.param(
            {"type": "type 1", "format": "format 1"},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="type 1", format="format 1")
            ),
            id="type with format",
        ),
        pytest.param(
            {"type": "type 1", "nullable": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="type 1", nullable=True)
            ),
            id="type with nullable",
        ),
        pytest.param(
            {"type": "type 1", "x-generated": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="type 1"),
                extension=_ColSchemaExtArtifacts(generated=True),
            ),
            id="type with x-generated",
        ),
        pytest.param(
            {"type": "type 1", "description": "description 1"},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(
                    type="type 1", description="description 1"
                )
            ),
            id="type with description",
        ),
        pytest.param(
            {"type": "string", "default": "value 1"},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="string", default="value 1")
            ),
            id="type with default",
        ),
        pytest.param(
            {"type": "string", "readOnly": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="string", read_only=True)
            ),
            id="type with readOnly",
        ),
        pytest.param(
            {"type": "string", "writeOnly": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="string", write_only=True)
            ),
            id="type with writeOnly",
        ),
        pytest.param(
            {"type": "string", "x-json": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="string"),
                extension=_ColSchemaExtArtifacts(json=True),
            ),
            id="simple type with x-json",
        ),
        pytest.param(
            {"type": "object", "x-json": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="object"),
                extension=_ColSchemaExtArtifacts(json=True),
            ),
            id="object type with x-json",
        ),
        pytest.param(
            {"type": "array", "x-json": True},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="array"),
                extension=_ColSchemaExtArtifacts(json=True),
            ),
            id="array type with x-json",
        ),
        pytest.param(
            {"type": "object", "x-de-$ref": "RefModel"},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="object"),
                extension=_ColSchemaExtArtifacts(de_ref="RefModel"),
            ),
            id="object",
        ),
        pytest.param(
            {"type": "array", "items": {"x-de-$ref": "RefModel"}},
            None,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="array"),
                extension=_ColSchemaExtArtifacts(de_ref="RefModel"),
            ),
            id="array",
        ),
        pytest.param(
            {"type": "type 1"},
            True,
            _ColSchemaArtifacts(
                open_api=_ColSchemaOAArtifacts(type="type 1", required=True)
            ),
            id="required given",
        ),
    ],
)
@pytest.mark.models_file
def test_gather_column_artifacts(schema, required, expected_artifacts):
    """
    GIVEN schema and required
    WHEN gather_column_artifacts is called with the schema and required
    THEN the given expected artifacts are returned.
    """
    artifacts = models_file._model._artifacts.gather_column_artifacts(
        schema=schema, required=required
    )

    assert artifacts == expected_artifacts


@pytest.mark.models_file
def test_calculate_name():
    """
    GIVEN name
    WHEN calculate is called with the name
    THEN the name is added to the artifacts.
    """
    schema = {"properties": {}}
    name = "Model"

    artifacts = models_file._model._artifacts.calculate(schema=schema, name=name)

    assert artifacts.sqlalchemy.name == name


@pytest.mark.parametrize(
    "schema, expected_description",
    [
        ({"properties": {}}, None),
        ({"description": "description 1", "properties": {}}, "description 1"),
    ],
    ids=["missing", "set"],
)
@pytest.mark.models_file
def test_calculate_description(schema, expected_description):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the description is added to the artifacts.
    """
    name = "Model"

    artifacts = models_file._model._artifacts.calculate(schema=schema, name=name)

    assert artifacts.sqlalchemy.description == expected_description


_EXPECTED_CLS_BASE = "typing.Protocol"
if sys.version_info[1] < 8:
    _EXPECTED_CLS_BASE = "typing_extensions.Protocol"


@pytest.mark.models_file
def test_calculate_parent():
    """
    GIVEN
    WHEN calculate is called
    THEN the correct parent class is set.
    """
    schema = {"properties": {}}

    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.parent_cls == _EXPECTED_CLS_BASE


@pytest.mark.parametrize(
    "schema, expected_columns",
    [
        ({"properties": {}}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}},
            [_ColumnArtifacts(name="column_1", type="typing.Optional[int]")],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                }
            },
            [
                _ColumnArtifacts(name="column_1", type="typing.Optional[int]"),
                _ColumnArtifacts(name="column_2", type="typing.Optional[str]"),
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [_ColumnArtifacts(name="column_1", type="int")],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [_ColumnArtifacts(name="column_1", type="typing.Optional[int]")],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer", "description": "description 1"}
                },
                "required": [],
            },
            [
                _ColumnArtifacts(
                    name="column_1",
                    type="typing.Optional[int]",
                    description="description 1",
                )
            ],
        ),
        ({"properties": {}, "x-backrefs": {}}, []),
        (
            {
                "properties": {},
                "x-backrefs": {"model": {"type": "object", "x-de-$ref": "Model"}},
            },
            [_ColumnArtifacts(name="model", type='typing.Optional["TModel"]')],
        ),
        (
            {
                "properties": {},
                "x-backrefs": {
                    "model1": {"type": "object", "x-de-$ref": "Model1"},
                    "model2": {"type": "object", "x-de-$ref": "Model2"},
                },
            },
            [
                _ColumnArtifacts(name="model1", type='typing.Optional["TModel1"]'),
                _ColumnArtifacts(name="model2", type='typing.Optional["TModel2"]'),
            ],
        ),
    ],
    ids=[
        "empty",
        "single",
        "multiple",
        "single in required",
        "single not in required",
        "single description",
        "empty x-backrefs",
        "single x-backrefs",
        "multiple x-backrefs",
    ],
)
@pytest.mark.models_file
def test_calculate_column(schema, expected_columns):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected columns are added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.columns == expected_columns


@pytest.mark.models_file
def test_calculate_column_inherits_return(mocked_facades_models):
    """
    GIVEN schema that inherits and mocked models facade
    WHEN calculate is called with the schema
    THEN the schema and parent schema columns are returned.
    """
    schema = {"properties": {"column_1": {"type": "integer"}}, "x-inherits": "Parent"}
    mocked_facades_models.get_model_schema.return_value = {
        "properties": {"column_2": {"type": "string"}}
    }

    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    mocked_facades_models.get_model_schema.assert_called_once_with(name="Parent")
    assert artifacts.sqlalchemy.columns == [
        _ColumnArtifacts(name="column_2", type="typing.Optional[str]"),
        _ColumnArtifacts(name="column_1", type="typing.Optional[int]"),
    ]


@pytest.mark.parametrize(
    "schema, expected_empty",
    [
        ({"properties": {}}, True),
        ({"properties": {"column_1": {"type": "integer"}}}, False),
    ],
    ids=["empty", "single"],
)
@pytest.mark.models_file
def test_calculate_empty(schema, expected_empty):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected empty is added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.empty == expected_empty


@pytest.mark.parametrize(
    "schema, expected_args",
    [
        ({"properties": {}}, []),
        ({"properties": {"column_1": {"type": "integer"}}}, []),
        ({"properties": {"column_1": {"type": "integer"}}, "required": []}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [
                _ColumnArgArtifacts(
                    name="column_1", init_type="int", from_dict_type="int"
                )
            ],
        ),
        (
            {
                "properties": {"column_1": {"type": "integer", "readOnly": True}},
                "required": ["column_1"],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="int",
                    from_dict_type="int",
                    read_only=True,
                )
            ],
        ),
        (
            {
                "properties": {"column_1": {"type": "object", "x-de-$ref": "RefModel"}},
                "required": ["column_1"],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type='"TRefModel"',
                    from_dict_type='"RefModelDict"',
                )
            ],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                },
                "required": ["column_1", "column_2"],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1", init_type="int", from_dict_type="int"
                ),
                _ColumnArgArtifacts(
                    name="column_2", init_type="str", from_dict_type="str"
                ),
            ],
        ),
    ],
    ids=[
        "empty",
        "single required not given",
        "single not required",
        "single required",
        "single readOnly",
        "single required object",
        "multiple required",
    ],
)
@pytest.mark.models_file
def test_calculate_required_args(schema, expected_args):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected required arguments are added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.arg.required == expected_args


@pytest.mark.parametrize(
    "schema, expected_args",
    [
        ({"properties": {}}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}},
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="typing.Optional[int]",
                    from_dict_type="typing.Optional[int]",
                )
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="typing.Optional[int]",
                    from_dict_type="typing.Optional[int]",
                )
            ],
        ),
        (
            {
                "properties": {"column_1": {"type": "integer", "nullable": False}},
                "required": [],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="typing.Optional[int]",
                    from_dict_type="typing.Optional[int]",
                )
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [],
        ),
        (
            {
                "properties": {"column_1": {"type": "integer", "default": 1}},
                "required": [],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1", init_type="int", from_dict_type="int", default=1
                )
            ],
        ),
        (
            {
                "properties": {
                    "column_1": {
                        "type": "string",
                        "format": "date",
                        "default": "2000-01-01",
                    }
                },
                "required": [],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="datetime.date",
                    from_dict_type="datetime.date",
                    default="datetime.date(2000, 1, 1)",
                )
            ],
        ),
        (
            {
                "properties": {"column_1": {"type": "object", "x-de-$ref": "RefModel"}},
                "required": [],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type='typing.Optional["TRefModel"]',
                    from_dict_type='typing.Optional["RefModelDict"]',
                )
            ],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                },
                "required": [],
            },
            [
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="typing.Optional[int]",
                    from_dict_type="typing.Optional[int]",
                ),
                _ColumnArgArtifacts(
                    name="column_2",
                    init_type="typing.Optional[str]",
                    from_dict_type="typing.Optional[str]",
                ),
            ],
        ),
    ],
    ids=[
        "empty",
        "single required not given",
        "single not required",
        "single not nullable not required",
        "single required",
        "single default",
        "single type mapped",
        "single not required object",
        "multiple not required",
    ],
)
@pytest.mark.models_file
def test_calculate_not_required_args(schema, expected_args):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the given expected td not required properties are added to the artifacts.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.sqlalchemy.arg.not_required == expected_args


class TestMapDefault:
    """Tests for _map_default."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, default, expected_default",
        [
            pytest.param(
                "integer",
                None,
                None,
                None,
                id="None",
            ),
            pytest.param(
                "integer",
                None,
                1,
                1,
                id="integer",
            ),
            pytest.param(
                "integer",
                "int32",
                1,
                1,
                id="integer int32",
            ),
            pytest.param(
                "integer",
                "int64",
                1,
                1,
                id="integer int64",
            ),
            pytest.param(
                "number",
                None,
                1.1,
                1.1,
                id="number",
            ),
            pytest.param(
                "number",
                "float",
                1.1,
                1.1,
                id="number float",
            ),
            pytest.param(
                "string",
                None,
                'value "1',
                '"value \\"1"',
                id="string",
            ),
            pytest.param(
                "string",
                "unsupported",
                'value "1',
                '"value \\"1"',
                id="string",
            ),
            pytest.param(
                "string",
                "password",
                'value "1',
                '"value \\"1"',
                id="string password",
            ),
            pytest.param(
                "string",
                "byte",
                'value "1',
                '"value \\"1"',
                id="string byte",
            ),
            pytest.param(
                "string",
                "binary",
                'value "1',
                'b"value \\"1"',
                id="string binary",
            ),
            pytest.param(
                "string",
                "date",
                "2000-01-01",
                "datetime.date(2000, 1, 1)",
                id="string date",
            ),
            pytest.param(
                "string",
                "date-time",
                "2000-01-01T01:01:01",
                "datetime.datetime(2000, 1, 1, 1, 1, 1)",
                id="string date-time",
            ),
            pytest.param(
                "boolean",
                None,
                True,
                True,
                id="boolean",
            ),
        ],
    )
    @pytest.mark.models_file
    def test_(type_, format_, default, expected_default):
        """
        GIVEN type, format and default
        WHEN _map_default is called with the artifacts
        THEN the expected default value is returned.
        """
        artifacts = _ColSchemaArtifacts(
            open_api=_ColSchemaOAArtifacts(type=type_, format=format_, default=default)
        )

        returned_default = models_file._model._artifacts._map_default(
            artifacts=artifacts
        )

        assert returned_default == expected_default
