"""Functions for model artifacts."""

import itertools
import json
import sys
import typing

from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import types
from . import type_ as _type


def gather_column_artifacts(
    schema: oa_types.Schema, required: typing.Optional[bool]
) -> types.ColumnSchemaArtifacts:
    """
    Gather artifacts for generating the class of a models.

    Assume the schema does not contain any $ref and allOf.
    Assume that the schema is an object with at least 1 property.
    Assume that each property has a type.

    Args:
        schema: The schema of the model.

    Returns:
        The artifacts for generating the class of a model.

    """
    type_ = helpers.peek.type_(schema=schema, schemas={})
    artifacts = types.ColumnSchemaArtifacts(
        open_api=types.ColumnSchemaOpenAPIArtifacts(type=type_, required=required)
    )
    artifacts.open_api.format = helpers.peek.format_(schema=schema, schemas={})
    artifacts.open_api.nullable = helpers.peek.nullable(schema=schema, schemas={})
    artifacts.open_api.description = helpers.peek.description(schema=schema, schemas={})
    artifacts.open_api.default = helpers.peek.default(schema=schema, schemas={})
    artifacts.open_api.read_only = helpers.peek.read_only(schema=schema, schemas={})
    artifacts.open_api.write_only = helpers.peek.write_only(schema=schema, schemas={})
    artifacts.extension.json = helpers.peek.json(schema=schema, schemas={})
    artifacts.extension.generated = helpers.ext_prop.get(
        source=schema, name="x-generated"
    )
    if not artifacts.extension.json:
        if type_ == "object":
            artifacts.extension.de_ref = helpers.ext_prop.get(
                source=schema, name="x-de-$ref"
            )
        if type_ == "array":
            artifacts.extension.de_ref = helpers.ext_prop.get(
                source=schema["items"], name="x-de-$ref"
            )

    return artifacts


def calculate(*, schema: oa_types.Schema, name: str) -> types.ModelArtifacts:
    """
    Calculate the model artifacts from the schema.

    Args:
        schema: The schema of the model
        name: The name of the model.

    Returns:
        The artifacts for the model.

    """
    # Resolve inheritance chain
    schema = helpers.inheritance.retrieve_model_parents_schema(schema=schema)

    required = set(schema.get("required", []))
    description = helpers.peek.description(schema=schema, schemas={})

    # Convert schemas to artifacts
    prop_schemas = schema["properties"].values()
    prop_required_list = [key in required for key in schema["properties"].keys()]
    columns_artifacts = list(
        map(gather_column_artifacts, prop_schemas, prop_required_list)
    )

    # Calculate artifacts for columns
    columns = list(
        map(_calculate_column_artifacts, schema["properties"].keys(), columns_artifacts)
    )
    # Calculate artifacts for the typed dictionary
    write_only_idx = [artifact.open_api.write_only for artifact in columns_artifacts]
    typed_dict_props = list(
        map(
            _calculate_typed_dict_artifacts,
            (
                value
                for idx, value in enumerate(schema["properties"].keys())
                if not write_only_idx[idx]
            ),
            (
                value
                for idx, value in enumerate(columns_artifacts)
                if not write_only_idx[idx]
            ),
        )
    )
    typed_dict_required_props = [
        typed_dict_prop
        for prop_required, typed_dict_prop in zip(prop_required_list, typed_dict_props)
        if prop_required
    ]
    typed_dict_not_required_props = [
        typed_dict_prop
        for prop_required, typed_dict_prop in zip(prop_required_list, typed_dict_props)
        if not prop_required
    ]
    # Calculate artifacts for the arguments
    args = list(
        map(_calculate_arg_artifacts, schema["properties"].keys(), columns_artifacts)
    )
    required_args = [
        arg for prop_required, arg in zip(prop_required_list, args) if prop_required
    ]
    not_required_args = [
        arg for prop_required, arg in zip(prop_required_list, args) if not prop_required
    ]
    # Calculate artifacts for back references
    backrefs = helpers.ext_prop.get(source=schema, name="x-backrefs")
    if backrefs is not None:
        backref_column_artifacts = map(
            gather_column_artifacts, backrefs.values(), itertools.repeat(None)
        )
        backref_columns_iter = map(
            _calculate_column_artifacts, backrefs.keys(), backref_column_artifacts
        )
        columns.extend(backref_columns_iter)

    # Calculate model parent class
    parent_cls: str
    if sys.version_info[1] < 8:
        parent_cls = "typing_extensions.Protocol"
    else:  # version compatibility
        parent_cls = "typing.Protocol"

    # Calculate whether property lists are empty, their names and parent class
    typed_dict_required_empty = not typed_dict_required_props
    typed_dict_not_required_empty = not typed_dict_not_required_props
    typed_dict_required_name = None
    typed_dict_not_required_name: typing.Optional[str] = f"{name}Dict"
    typed_dict_required_parent_class = None
    typed_dict_not_required_parent_class: typing.Optional[str]
    if sys.version_info[1] < 8:
        typed_dict_not_required_parent_class = "typing_extensions.TypedDict"
    else:  # version compatibility
        typed_dict_not_required_parent_class = "typing.TypedDict"
    if not typed_dict_required_empty and not typed_dict_not_required_empty:
        typed_dict_required_parent_class = typed_dict_not_required_parent_class
        typed_dict_required_name = f"_{name}DictBase"
        typed_dict_not_required_parent_class = typed_dict_required_name
    if not typed_dict_required_empty and typed_dict_not_required_empty:
        typed_dict_required_name = typed_dict_not_required_name
        typed_dict_not_required_name = None
        typed_dict_required_parent_class = typed_dict_not_required_parent_class
        typed_dict_not_required_parent_class = None

    return types.ModelArtifacts(
        sqlalchemy=types.SQLAlchemyModelArtifacts(
            name=name,
            columns=columns,
            empty=not columns,
            arg=types.ArgArtifacts(
                required=required_args, not_required=not_required_args
            ),
            parent_cls=parent_cls,
            description=description,
        ),
        typed_dict=types.TypedDictArtifacts(
            required=types.TypedDictClassArtifacts(
                props=typed_dict_required_props,
                empty=typed_dict_required_empty,
                name=typed_dict_required_name,
                parent_class=typed_dict_required_parent_class,
            ),
            not_required=types.TypedDictClassArtifacts(
                props=typed_dict_not_required_props,
                empty=typed_dict_not_required_empty,
                name=typed_dict_not_required_name,
                parent_class=typed_dict_not_required_parent_class,
            ),
        ),
    )


def _calculate_column_artifacts(
    name: str, artifacts: types.ColumnSchemaArtifacts
) -> types.ColumnArtifacts:
    """Calculate column artifacts from schema artifacts."""
    # Calculate the type
    type_ = _type.model(artifacts=artifacts)

    # Add artifacts to the lists
    return types.ColumnArtifacts(
        type=type_,
        name=name,
        description=artifacts.open_api.description,
    )


def _calculate_typed_dict_artifacts(
    name: str, artifacts: types.ColumnSchemaArtifacts
) -> types.ColumnArtifacts:
    """Calculate typed dict artifacts from schema artifacts."""
    # Calculate the type
    type_ = _type.typed_dict(artifacts=artifacts)

    # Add artifacts to the lists
    return types.ColumnArtifacts(
        type=type_,
        name=name,
        description=artifacts.open_api.description,
    )


def _calculate_arg_artifacts(
    name: str, artifacts: types.ColumnSchemaArtifacts
) -> types.ColumnArgArtifacts:
    """Calculate typed dict artifacts from schema artifacts."""
    # Calculate the type
    init_type = _type.arg_init(artifacts=artifacts)
    from_dict_type = _type.arg_from_dict(artifacts=artifacts)

    # Add artifacts to the lists
    return types.ColumnArgArtifacts(
        init_type=init_type,
        from_dict_type=from_dict_type,
        name=name,
        default=_map_default(artifacts=artifacts),
        read_only=artifacts.open_api.read_only,
    )


def _map_default(*, artifacts: types.ColumnSchemaArtifacts) -> oa_types.TColumnDefault:
    """
    Map default value from OpenAPI to be ready to be inserted into a Python file.

    First applies JSON formatting for a string and then using the type mapping helper
    function.

    Args:
        artifacts: The artifacts from which to map the default value.

    Returns:
        The mapped default value.

    """
    default = artifacts.open_api.default
    if default is None:
        return None

    # Escape string
    if artifacts.open_api.type == "string" and artifacts.open_api.format not in {
        "date",
        "date-time",
    }:
        default = json.dumps(default)

    # Handle bytes
    if artifacts.open_api.type == "string" and artifacts.open_api.format == "binary":
        return f"b{default}"

    # Map type
    mapped_default = helpers.oa_to_py_type.convert(
        value=default, type_=artifacts.open_api.type, format_=artifacts.open_api.format
    )

    # Get the repr if it isn't a float, bool, number nor str
    if isinstance(mapped_default, (int, float, str, bool)):
        return mapped_default
    return repr(mapped_default)
