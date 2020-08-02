"""Validate the schema of a model."""

# pylint: disable=unused-argument

import itertools

from ... import exceptions
from ... import helpers as oa_helpers
from ... import types as oa_types
from .. import helpers
from . import types


def _check_properties(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check properties."""
    # Check property values
    properties_values = helpers.iterate.properties_values(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    any_properties_value_not_list = any(
        filter(
            lambda properties_value: not isinstance(properties_value, dict),
            properties_values,
        )
    )
    if any_properties_value_not_list:
        return types.Result(False, "value of properties must be a dictionary")

    # Check there is at least a single property
    properties_items = helpers.iterate.property_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    first_property = next(properties_items, None)
    if first_property is None:
        return types.Result(False, "models must have at least 1 property themself")
    properties_items = itertools.chain([first_property], properties_items)

    # Check that all property names are strings
    property_names = map(lambda prop: prop[0], properties_items)
    any_property_name_not_string = any(
        filter(lambda property_name: not isinstance(property_name, str), property_names)
    )
    if any_property_name_not_string:
        return types.Result(False, "properties :: all property keys must be strings")

    return None


def _check_required(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check required."""
    # Retrieve property names
    properties_items = helpers.iterate.property_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    property_name_set = set(map(lambda prop: prop[0], properties_items))

    # Check that all required values are lists
    required_values = helpers.iterate.required_values(schema=schema, schemas=schemas)
    any_required_value_not_list = any(
        filter(
            lambda required_value: not isinstance(required_value, list), required_values
        )
    )
    if any_required_value_not_list:
        return types.Result(False, "value of required must be a list")

    # Check required values
    required_items = helpers.iterate.required_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    required_items_set = set(required_items)
    any_required_items_not_string = any(
        filter(
            lambda required_item: not isinstance(required_item, str), required_items_set
        )
    )
    if any_required_items_not_string:
        return types.Result(False, "required :: all items must be strings")

    # Check that all required items are property names
    required_not_properties = required_items_set - property_name_set
    if required_not_properties:
        return types.Result(
            False,
            "required :: all items must be properties, "
            f"{next(iter(required_not_properties))} is not",
        )

    return None


def _check_mandatory(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check mandatory keys of the model schema."""
    # Check for inheritance
    inherits = oa_helpers.schema.inherits(schema=schema, schemas=schemas)
    if inherits:
        oa_helpers.inheritance.get_parent(schema=schema, schemas=schemas)

    tablename = oa_helpers.peek.tablename(schema=schema, schemas=schemas)
    if tablename is None and not inherits:
        return types.Result(False, "every model must define x-tablename")

    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ != "object":
        return types.Result(False, "models must have the object type")

    properties_result = _check_properties(schema=schema, schemas=schemas)
    if properties_result is not None:
        return properties_result

    return None


def _check_kwargs(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check kwargs value of it exists."""
    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)
    if kwargs is None:
        return None

    def invalid_key(key) -> bool:
        """Check value of key is valid."""
        assert isinstance(key, str)
        return not key.startswith("__") or not key.endswith("__")

    kwargs_keys = list(kwargs.keys())
    any_kwargs_keys_invalid = any(filter(invalid_key, kwargs_keys,))
    if any_kwargs_keys_invalid:
        return types.Result(
            False, "models x-kwargs must have keys that start and end with __"
        )
    if "__table_args__" in kwargs:
        return types.Result(False, "models x-kwargs cannot define __table_args__")

    return None


def _check_invalid_keys(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check for keys that are not valid on a model."""
    invalid_keys = (
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key",
        "x-foreign-key-kwargs",
    )
    seen_invalid_keys = filter(
        lambda key: oa_helpers.peek.peek_key(schema=schema, schemas=schemas, key=key)
        is not None,
        invalid_keys,
    )
    invalid_key = next(seen_invalid_keys, None)
    if invalid_key is not None:
        return types.Result(False, f"models do not support the {invalid_key} key")

    return None


def _check_modifiers(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check basics related to tablename, inheritance and type."""
    required_result = _check_required(schema=schema, schemas=schemas)
    if required_result is not None:
        return required_result

    # Check description value
    oa_helpers.peek.description(schema=schema, schemas=schemas)

    # Check kwargs
    kwargs_result = _check_kwargs(schema=schema, schemas=schemas)
    if kwargs_result is not None:
        return kwargs_result

    # Check for invalid keys
    invalid_keys_result = _check_invalid_keys(schema=schema, schemas=schemas)
    if invalid_keys_result is not None:
        return invalid_keys_result

    return None


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check that a schema is valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema to validate.

    Returns:
        Whether the schema is valid with the reason if it is not.

    """
    try:
        mandatory_result = _check_mandatory(schema=schema, schemas=schemas)
        if mandatory_result is not None:
            return mandatory_result
        modifiers_result = _check_modifiers(schema=schema, schemas=schemas)
        if modifiers_result is not None:
            return modifiers_result

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")
    except exceptions.MalformedExtensionPropertyError as exc:
        return types.Result(False, f"sextension property :: {exc}")

    return types.Result(True, None)
