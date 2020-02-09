"""Generate model from OpenAPI schema."""

import itertools
import typing

from . import column_factory
from . import exceptions
from . import helpers
from . import table_args
from . import types
from . import utility_base


def model_factory(
    *, name: str, base: typing.Type, schemas: types.Schemas
) -> typing.Type:
    """
    Convert OpenAPI schema to SQLAlchemy model.

    Args:
        name: The name of the schema.
        base: The SQLAlchemy declarative base.
        schemas: The OpenAPI schemas.

    Returns:
        The model as a class.

    """
    # Input validation
    # Checking that name is in schemas
    if name not in schemas:
        raise exceptions.SchemaNotFoundError(f"{name} not found in schemas")
    schema: types.Schema = schemas.get(name, {})
    # De-referencing schema
    schema = helpers.prepare_schema(schema=schema, schemas=schemas)
    # Checking for tablename key
    if "x-tablename" not in schema:
        raise exceptions.MalformedSchemaError(
            f'"x-tablename" is a required schema property for {name}.'
        )
    # Checking for object type
    if schema.get("type") != "object":
        raise exceptions.FeatureNotImplementedError(
            f"{schema.get('type')} is not supported in {name}."
        )
    if not schema.get("properties"):
        raise exceptions.MalformedSchemaError(
            f"At least 1 property is required for {name}."
        )

    # Calculating the class variables for the model
    model_class_vars = []
    required_exists = "required" in schema
    required_array = schema.get("required", [])
    required_set = set(required_array)
    # Initializing the schema to record for the model
    model_schema: types.Schema = {"type": "object", "properties": {}}
    if required_exists:
        model_schema["required"] = required_array
    if "x-backrefs" in schema:
        model_schema["x-backrefs"] = helpers.get_ext_prop(
            source=schema, name="x-backrefs"
        )
    description = helpers.peek.description(schema=schema, schemas={})
    if description is not None:
        model_schema["description"] = description
    for prop_name, prop_spec in schema.get("properties", []).items():
        prop_class_vars, prop_final_spec = column_factory.column_factory(
            spec=prop_spec,
            schemas=schemas,
            logical_name=prop_name,
            required=prop_name in required_set if required_exists else None,
            model_schema=schema,
            model_name=name,
        )
        model_class_vars.append(prop_class_vars)
        dict_ignore = helpers.get_ext_prop(
            source=prop_final_spec, name="x-dict-ignore", default=False, pop=True
        )
        if not dict_ignore:
            model_schema["properties"][prop_name] = prop_final_spec

    # Assembling model
    return type(
        name,
        (base, utility_base.UtilityBase),
        {
            "__tablename__": helpers.get_ext_prop(source=schema, name="x-tablename"),
            "_schema": model_schema,
            **dict(itertools.chain.from_iterable(model_class_vars)),
            "__table_args__": table_args.construct(schema=schema),
        },
    )
