"""Generate model from OpenAPI schema."""

import typing

from . import column_factory
from . import exceptions
from . import mixins
from . import table_args
from . import types
from . import utility_base
from .helpers import ext_prop
from .helpers import inheritance
from .helpers import peek
from .helpers import ref
from .helpers import schema as schema_helper


class GetBase(types.Protocol):
    """Defines interface for the get_base function."""

    def __call__(self, *, name: str, schemas: types.Schemas) -> typing.Type:
        """Call signature for get_base."""
        ...


def model_factory(
    *,
    name: str,
    get_base: GetBase,
    schemas: types.Schemas,
    artifacts: types.ModelsModelArtifacts,
) -> typing.Type:
    """
    Convert OpenAPI schema to SQLAlchemy model.

    Args:
        name: The name of the schema.
        get_base: Funcrtion to retrieve the base class for the model.
        schemas: The OpenAPI schemas.
        artifacts: The artifacts for the models.

    Returns:
        The model as a class.

    """
    schema = _get_schema(name, schemas)
    artifacts_name, _ = ref.resolve(name=name, schema=schemas[name], schemas=schemas)
    model_artifacts = artifacts.get(artifacts_name)
    assert model_artifacts is not None

    # Calculating the class variables for the model
    model_class_vars = {}
    required_exists = types.OpenApiProperties.REQUIRED in schema
    required_array = schema.get(types.OpenApiProperties.REQUIRED, [])
    # Initializing the schema to record for the model
    model_schema: types.Schema = {
        types.OpenApiProperties.TYPE: "object",
        types.OpenApiProperties.PROPERTIES: {},
    }
    if required_exists:
        model_schema[types.OpenApiProperties.REQUIRED] = required_array
    inherits = peek.inherits(schema=schema, schemas={})
    if inherits is not None:
        model_schema[types.ExtensionProperties.INHERITS] = inherits
    description = peek.description(schema=schema, schemas={})
    if description is not None:
        model_schema[types.OpenApiProperties.DESCRIPTION.value] = description

    for prop_name, prop_artifacts in model_artifacts.properties:
        prop_column = column_factory.column_factory(artifacts=prop_artifacts)
        if prop_column is not None:
            model_class_vars[prop_name] = prop_column

        dict_ignore = (
            prop_artifacts.type == types.PropertyType.SIMPLE
            and prop_artifacts.extension.dict_ignore
        )

        if not dict_ignore:
            model_schema[types.OpenApiProperties.PROPERTIES][
                prop_name
            ] = prop_artifacts.schema

    # Retrieve mixins
    mixin_classes: typing.Tuple[typing.Type, ...] = tuple()
    mixin_values = peek.mixins(schema=schema, schemas=schemas)
    if mixin_values is not None:
        mixin_classes = mixins.get(mixins=mixin_values)

    # Assembling model
    base = get_base(name=name, schemas=schemas)
    return type(
        name,
        (base, utility_base.UtilityBase, *mixin_classes),
        {
            "_schema": model_schema,
            **model_class_vars,
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
    inherits = schema_helper.inherits(schema=schema, schemas=schemas)
    if not inherits:
        # De-referencing schema
        schema = schema_helper.prepare(schema=schema, schemas=schemas)
        # Checking for tablename key
        tablename = peek.tablename(schema=schema, schemas={})
        if tablename is None:
            raise exceptions.MalformedSchemaError(
                f'"{types.ExtensionProperties.TABLENAME}" is a required schema '
                f"property for {name}."
            )
    else:
        parent = inheritance.retrieve_parent(schema=schema, schemas=schemas)
        # De-referencing schema excluding parent schema
        schema = schema_helper.prepare(schema=schema, schemas=schemas, skip_name=parent)
        # Checking for inherits key
        inherits_schema_value = peek.inherits(schema=schema, schemas={})
        if inherits_schema_value is None:
            raise exceptions.MalformedSchemaError(
                f'"{types.ExtensionProperties.INHERITS}" is a required schema property '
                f"for {name}."
            )
        schema[types.ExtensionProperties.INHERITS] = parent
    # Checking for object type
    type_ = schema.get(types.OpenApiProperties.TYPE)
    if type_ != "object":
        raise exceptions.FeatureNotImplementedError(
            f"{type_} is not supported in {name}."
        )
    if not schema.get(types.OpenApiProperties.PROPERTIES):
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
    kwargs = ext_prop.get_kwargs(
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
    tablename = peek.tablename(schema=schema, schemas={})
    if tablename is not None:
        return {"__tablename__": tablename}
    return {}
