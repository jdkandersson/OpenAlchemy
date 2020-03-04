"""Functions for model artifacts."""

import json
import sys
import typing

from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import types
from . import type_ as _type


def gather_column_artifacts(
    *, schema: oa_types.Schema, required: typing.Optional[bool]
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
    format_ = helpers.peek.format_(schema=schema, schemas={})
    nullable = helpers.peek.nullable(schema=schema, schemas={})
    description = helpers.peek.description(schema=schema, schemas={})
    default = helpers.peek.default(schema=schema, schemas={})
    generated = helpers.get_ext_prop(source=schema, name="x-generated")
    de_ref = None
    if type_ == "object":
        de_ref = helpers.get_ext_prop(source=schema, name="x-de-$ref")
    if type_ == "array":
        de_ref = helpers.get_ext_prop(source=schema["items"], name="x-de-$ref")

    return types.ColumnSchemaArtifacts(
        type=type_,
        format=format_,
        nullable=nullable,
        required=required,
        de_ref=de_ref,
        generated=generated,
        description=description,
        default=default,
    )


def calculate(*, schema: oa_types.Schema, name: str) -> types.ModelArtifacts:
    """
    Calculate the model artifacts from the schema.

    Args:
        schema: The schema of the model
        name: The name of the model.

    Returns:
        The artifacts for the model.

    """
    required = set(schema.get("required", []))
    description = helpers.peek.description(schema=schema, schemas={})

    # Initialize lists
    columns: typing.List[types.ColumnArtifacts] = []
    td_required_props: typing.List[types.ColumnArtifacts] = []
    td_not_required_props: typing.List[types.ColumnArtifacts] = []
    required_args: typing.List[types.ColumnArgArtifacts] = []
    not_required_args: typing.List[types.ColumnArgArtifacts] = []

    # Calculate artifacts for properties
    for property_name, property_schema in schema["properties"].items():
        # Gather artifacts
        property_required = property_name in required
        column_artifacts = gather_column_artifacts(
            schema=property_schema, required=property_required
        )

        # Calculate the type
        column_type = _type.model(artifacts=column_artifacts)
        td_prop_type = _type.typed_dict(artifacts=column_artifacts)
        arg_init_type = _type.arg_init(artifacts=column_artifacts)
        arg_from_dict_type = _type.arg_from_dict(artifacts=column_artifacts)

        # Add artifacts to the lists
        columns.append(
            types.ColumnArtifacts(
                type=column_type,
                name=property_name,
                description=column_artifacts.description,
            )
        )
        prop_artifacts = types.ColumnArtifacts(type=td_prop_type, name=property_name)
        arg_artifacts = types.ColumnArgArtifacts(
            init_type=arg_init_type,
            from_dict_type=arg_from_dict_type,
            name=property_name,
            default=_map_default(artifacts=column_artifacts),
        )
        if property_required:
            td_required_props.append(prop_artifacts)
            required_args.append(arg_artifacts)
        else:
            td_not_required_props.append(prop_artifacts)
            not_required_args.append(arg_artifacts)

    # Calculate artifacts for back references
    backrefs = helpers.get_ext_prop(source=schema, name="x-backrefs")
    if backrefs is not None:
        for backref_name, backref_schema in backrefs.items():
            # Gather artifacts
            column_artifacts = gather_column_artifacts(
                schema=backref_schema, required=None
            )

            # Calculate the type
            column_type = _type.model(artifacts=column_artifacts)

            # Add artifacts to the lists
            columns.append(types.ColumnArtifacts(type=column_type, name=backref_name))

    # Calculate model parent class
    parent_cls: str
    if sys.version_info[1] < 8:
        parent_cls = "typing_extensions.Protocol"
    else:  # version compatibility
        parent_cls = "typing.Protocol"

    # Calculate whether property lists are empty, their names and parent class
    td_required_empty = not td_required_props
    td_not_required_empty = not td_not_required_props
    td_required_name = None
    td_not_required_name: typing.Optional[str] = f"{name}Dict"
    td_required_parent_class = None
    td_not_required_parent_class: typing.Optional[str]
    if sys.version_info[1] < 8:
        td_not_required_parent_class = "typing_extensions.TypedDict"
    else:  # version compatibility
        td_not_required_parent_class = "typing.TypedDict"
    if not td_required_empty and not td_not_required_empty:
        td_required_parent_class = td_not_required_parent_class
        td_required_name = f"_{name}DictBase"
        td_not_required_parent_class = td_required_name
    if not td_required_empty and td_not_required_empty:
        td_required_name = td_not_required_name
        td_not_required_name = None
        td_required_parent_class = td_not_required_parent_class
        td_not_required_parent_class = None

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
                props=td_required_props,
                empty=td_required_empty,
                name=td_required_name,
                parent_class=td_required_parent_class,
            ),
            not_required=types.TypedDictClassArtifacts(
                props=td_not_required_props,
                empty=td_not_required_empty,
                name=td_not_required_name,
                parent_class=td_not_required_parent_class,
            ),
        ),
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
    default = artifacts.default
    if default is None:
        return None

    # Escape string
    if artifacts.type == "string" and artifacts.format not in {"date", "date-time"}:
        default = json.dumps(default)

    # Handle bytes
    if artifacts.type == "string" and artifacts.format == "binary":
        return f"b{default}"

    # Map type
    mapped_default = helpers.oa_to_py_type.convert(
        value=default, type_=artifacts.type, format_=artifacts.format
    )

    # Get the repr if it isn't a float, bool, number nor str
    if isinstance(mapped_default, (int, float, str, bool)):
        return mapped_default
    return repr(mapped_default)
