"""Generate model from OpenAPI schema."""

import itertools
import typing

from . import column_factory
from . import exceptions
from . import helpers
from . import mixins
from . import table_args
from . import types
from . import utility_base


def model_factory(
    *, name: str, get_base: types.GetBase, schemas: types.Schemas
) -> typing.Type:
    """
    Convert OpenAPI schema to SQLAlchemy model.

    Args:
        name: The name of the schema.
        get_base: Funcrtion to retrieve the base class for the model.
        schemas: The OpenAPI schemas.

    Returns:
        The model as a class.

    """
    schema = _get_schema(name, schemas)

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
        model_schema["x-backrefs"] = helpers.ext_prop.get(
            source=schema, name="x-backrefs"
        )
    if "x-inherits" in schema:
        model_schema["x-inherits"] = helpers.ext_prop.get(
            source=schema, name="x-inherits"
        )
    description = helpers.peek.description(schema=schema, schemas={})
    if description is not None:
        model_schema["description"] = description
    for prop_name, prop_spec in schema.get("properties", []).items():
        prop_class_vars, prop_final_spec = column_factory.column_factory(
            schema=prop_spec,
            schemas=schemas,
            logical_name=prop_name,
            required=prop_name in required_set if required_exists else None,
            model_schema=schema,
        )
        model_class_vars.append(prop_class_vars)
        dict_ignore = helpers.ext_prop.get(
            source=prop_final_spec, name="x-dict-ignore", default=False, pop=True
        )
        if not dict_ignore:
            model_schema["properties"][prop_name] = prop_final_spec

    # Retrieve mixins
    mixin_classes: typing.Tuple[typing.Type, ...] = tuple()
    mixin_values = helpers.peek.mixins(schema=schema, schemas=schemas)
    if mixin_values is not None:
        mixin_classes = mixins.get(mixins=mixin_values)

    # Assembling model
    base = get_base(name=name, schemas=schemas)
    return type(
        name,
        (base, utility_base.UtilityBase, *mixin_classes),
        {
            "_schema": model_schema,
            **dict(itertools.chain.from_iterable(model_class_vars)),
            "__table_args__": table_args.construct(schema=schema),
            **_get_kwargs(schema=schema),
            **_prepare_model_dict(schema=schema),
            "__abstract__": False,
        },
    )


def _get_schema(name: str, schemas: types.Schemas) -> types.Schema:
    """
    Retrieve and prepare the schema from the schemas.

    Assume the schema has already been prepared. Replace x-inherits boolean with the
    parent name.

    Raise SchemaNotFoundError if the schema is not found in the schemas.
    Raise MalformedSchemaError is the schema does not have x-tablename.
    Raise FeatureNotImplementedError if the type is not found or it is not "object".
    Raise MalformedSchemaError if there are no properties.

    Args:
        name: The name of the schema to retrieve.
        schemas: All the schemas.

    Returns:
        The schema.

    """
    # Input validation
    # Checking that name is in schemas
    if name not in schemas:
        raise exceptions.SchemaNotFoundError(f"{name} not found in schemas")
    schema: types.Schema = schemas.get(name, {})
    # Check for parent
    inherits = helpers.schema.inherits(schema=schema, schemas=schemas)
    if not inherits:
        # De-referencing schema
        schema = helpers.schema.prepare(schema=schema, schemas=schemas)
        # Checking for tablename key
        if "x-tablename" not in schema:
            raise exceptions.MalformedSchemaError(
                f'"x-tablename" is a required schema property for {name}.'
            )
    else:
        parent = helpers.inheritance.retrieve_parent(schema=schema, schemas=schemas)
        # De-referencing schema excluding parent schema
        schema = helpers.schema.prepare(
            schema=schema, schemas=schemas, skip_name=parent
        )
        # Checking for inherits key
        if "x-inherits" not in schema:
            raise exceptions.MalformedSchemaError(
                f'"x-inherits" is a required schema property for {name}.'
            )
        schema["x-inherits"] = parent
    # Checking for object type
    if schema.get("type") != "object":
        raise exceptions.FeatureNotImplementedError(
            f"{schema.get('type')} is not supported in {name}."
        )
    if not schema.get("properties"):
        raise exceptions.MalformedSchemaError(
            f"At least 1 property is required for {name}."
        )
    return schema


def _get_kwargs(*, schema: types.Schema) -> types.TKwargs:
    """
    Retrieve kwargs for for the model.

    Raise MalformedExtensionPropertyError is the key does not start and end with __.

    Args:
        schema: The schema of the model.

    Returns:
        The kwargs for the model.

    """
    kwargs = helpers.ext_prop.get_kwargs(
        source=schema, reserved={"__tablename__", "__table_args__"}
    )
    if kwargs is None:
        return {}
    # Check that key starts and ends with __
    if any(not key.startswith("__") or not key.endswith("__") for key in kwargs.keys()):
        raise exceptions.MalformedExtensionPropertyError(
            "Model kwargs can only start and end with '__'."
        )
    return kwargs


def _prepare_model_dict(schema: types.Schema) -> typing.Dict[str, typing.Any]:
    """
    Prepare the dictionary used to construct the model.

    Assume the schema is valid.
    Add the __tablename__ key if it is required.

    Args:
        name: The name of the schema to prepare the dictionary for.
        schemas: All the schemas.

    Returns:
        The dictionary for the schema.

    """
    tablename = helpers.peek.tablename(schema=schema, schemas={})
    if tablename is not None:
        return {"__tablename__": tablename}
    return {}
