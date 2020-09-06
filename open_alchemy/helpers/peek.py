"""Assemble the final schema and return its type."""

import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types

from . import ext_prop as ext_prop_helper
from . import ref as ref_helper


class PeekValue(types.Protocol):
    """Defines interface for peek functions."""

    def __call__(self, *, schema: types.Schema, schemas: types.Schemas) -> typing.Any:
        """Call signature for peek functions."""
        ...


def type_(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the type of the schema.

    Raises TypeMissingError if the final schema does not have a type or the value is
    not a string.

    Args:
        schema: The schema for which to get the type.
        schemas: The schemas for $ref lookup.

    Returns:
        The type of the schema.

    """
    value = peek_key(schema=schema, schemas=schemas, key="type")
    if value is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    if not isinstance(value, str):
        raise exceptions.TypeMissingError(
            "A type property value must be of type string."
        )
    return value


def nullable(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the nullable property from a property schema.

    Raises MalformedSchemaError if the nullable value is not a boolean.

    Args:
        schema: The schema to get the nullable from.
        schemas: The schemas for $ref lookup.

    Returns:
        The nullable value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="nullable")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A nullable value must be of type boolean."
        )
    return value


def format_(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the format property from a property schema.

    Raises MalformedSchemaError if the format value is not a string.

    Args:
        schema: The schema to get the format from.
        schemas: The schemas for $ref lookup.

    Returns:
        The format value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="format")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError("A format value must be of type string.")
    return value


def autoincrement(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[bool]:
    """
    Retrieve the x-autoincrement property from a property schema.

    Raises MalformedSchemaError if the x-autoincrement value is not a boolean.

    Args:
        schema: The schema to get the x-autoincrement from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-autoincrement value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-autoincrement")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A autoincrement value must be of type boolean."
        )
    return value


def index(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the x-index property from a property schema.

    Raises MalformedSchemaError if the x-index value is not a boolean.

    Args:
        schema: The schema to get the x-index from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-index value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-index")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError("A index value must be of type boolean.")
    return value


def unique(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the x-unique property from a property schema.

    Raises MalformedSchemaError if the x-unique value is not a boolean.

    Args:
        schema: The schema to get the x-unique from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-unique value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-unique")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError("A unique value must be of type boolean.")
    return value


def max_length(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[int]:
    """
    Retrieve the maxLength property from a property schema.

    Raises MalformedSchemaError if the maxLength value is not an integer.

    Args:
        schema: The schema to get the maxLength from.
        schemas: The schemas for $ref lookup.

    Returns:
        The maxLength value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="maxLength")
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A maxLength value must be of type integer."
        )
    return value


def read_only(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Determine whether schema is readOnly.

    Raises MalformedSchemaError if the readOnly value is not a boolean.

    Args:
        schema: The schema to get readOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is readOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="readOnly")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A readOnly property must be of type boolean."
        )
    return value


def write_only(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[bool]:
    """
    Determine whether schema is writeOnly.

    Raises MalformedSchemaError if the writeOnly value is not a boolean.

    Args:
        schema: The schema to get writeOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is writeOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="writeOnly")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A writeOnly property must be of type boolean."
        )
    return value


def description(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the description property from a property schema.

    Raises MalformedSchemaError if the description value is not a string.

    Args:
        schema: The schema to get the description from.
        schemas: The schemas for $ref lookup.

    Returns:
        The description value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="description")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "A description value must be of type string."
        )
    return value


def primary_key(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Determine whether property schema is for a primary key.

    Raises MalformedSchemaError if the x-primary-key value is not a boolean.

    Args:
        schema: The schema to get x-primary-key from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is for a primary key property.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-primary-key")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-primary-key property must be of type boolean."
        )
    return value


def tablename(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the x-tablename of the schema.

    Raises MalformedSchemaError if the x-tablename value is not a string.

    Args:
        schema: The schema to get x-tablename from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-tablename or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-tablename")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-tablename property must be of type string."
        )
    return value


def inherits(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.Union[str, bool]]:
    """
    Retrieve the value of the x-inherits extension property of the schema.

    Raises MalformedSchemaError if the value is not a string nor a boolean.

    Args:
        schema: The schema to get x-inherits from.
        schemas: The schemas for $ref lookup.

    Returns:
        The inherits or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-inherits")
    if value is None:
        return None
    if not isinstance(value, (str, bool)):
        raise exceptions.MalformedSchemaError(
            "The x-inherits property must be of type string or boolean."
        )
    return value


def json(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the value of the x-json extension property of the schema.

    Raises MalformedSchemaError if the value is not a boolean.

    Args:
        schema: The schema to get x-json from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-json value or None if the schema does not have the key.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-json")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-json property must be of type boolean."
        )
    return value


def backref(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the x-backref of the schema.

    Raises MalformedSchemaError if the x-backref value is not a string.

    Args:
        schema: The schema to get x-backref from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-backref or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-backref")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-backref property must be of type string."
        )
    return value


def secondary(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the x-secondary of the schema.

    Raises MalformedSchemaError if the x-secondary value is not a string.

    Args:
        schema: The schema to get x-secondary from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-secondary or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-secondary")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-secondary property must be of type string."
        )
    return value


def uselist(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the x-uselist of the schema.

    Raises MalformedSchemaError if the x-uselist value is not a boolean.

    Args:
        schema: The schema to get x-uselist from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-uselist or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-uselist")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-uselist property must be of type boolean."
        )
    return value


def items(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[dict]:
    """
    Retrieve the items of the schema.

    Raises MalformedSchemaError if the items value is not a dictionary.

    Args:
        schema: The schema to get items from.
        schemas: The schemas for $ref lookup.

    Returns:
        The items or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="items")
    if value is None:
        return None
    if not isinstance(value, dict):
        raise exceptions.MalformedSchemaError(
            "The items property must be of type dict."
        )
    return value


def _check_kwargs(*, value: typing.Any, key: str) -> typing.Dict[str, typing.Any]:
    """Check the kwargs value."""
    # Check value
    if not isinstance(value, dict):
        raise exceptions.MalformedSchemaError(
            f"The {key} property must be of type dict."
        )
    # Check keys
    not_str_keys = filter(lambda key: not isinstance(key, str), value.keys())
    if next(not_str_keys, None) is not None:
        raise exceptions.MalformedSchemaError(
            f"The {key} property must have string keys."
        )
    return value


def kwargs(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """
    Retrieve the x-kwargs of the schema.

    Raises MalformedSchemaError if the x-kwargs value is not a dictionary.

    Args:
        schema: The schema to get x-kwargs from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-kwargs or None.

    """
    key = "x-kwargs"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    return _check_kwargs(value=value, key=key)


def foreign_key_kwargs(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[dict]:
    """
    Retrieve the x-foreign-key-kwargs of the schema.

    Raises MalformedSchemaError if the x-foreign-key-kwargs value is not a dictionary.

    Args:
        schema: The schema to get x-foreign-key-kwargs from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-foreign-key-kwargs or None.

    """
    key = "x-foreign-key-kwargs"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    return _check_kwargs(value=value, key=key)


def ref(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the $ref of the schema.

    Raises MalformedSchemaError if the $ref value is not a dictionary.

    Args:
        schema: The schema to get $ref from.
        schemas: The schemas for $ref lookup.

    Returns:
        The $ref or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="$ref")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The $ref property must be of type string."
        )
    return value


def foreign_key(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the x-foreign-key of the schema.

    Raises MalformedSchemaError if the x-foreign-key value is not a string.

    Args:
        schema: The schema to get x-foreign-key from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-foreign-key or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-foreign-key")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-foreign-key property must be of type string."
        )
    return value


def foreign_key_column(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the x-foreign-key-column of the schema.

    Raises MalformedSchemaError if the x-foreign-key-column value is not a string.

    Args:
        schema: The schema to get x-foreign-key-column from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-foreign-key-column or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-foreign-key-column")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-foreign-key-column property must be of type string."
        )
    return value


def composite_index(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.List]:
    """
    Retrieve the x-composite-index of the schema.

    Args:
        schema: The schema to get x-composite-index from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-composite-index or None.

    """
    key = "x-composite-index"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    ext_prop_helper.get(source={key: value}, name=key)  # type: ignore
    return value


def composite_unique(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.List]:
    """
    Retrieve the x-composite-unique of the schema.

    Args:
        schema: The schema to get x-composite-unique from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-composite-unique or None.

    """
    key = "x-composite-unique"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    ext_prop_helper.get(source={key: value}, name=key)  # type: ignore
    return value


def default(*, schema: types.Schema, schemas: types.Schemas) -> types.TColumnDefault:
    """
    Retrieve the default value and check it against the schema.

    Raises MalformedSchemaError if the default value does not conform with the schema.

    Args:
        schema: The schema to retrieve the default value from.

    Returns:
        The default or None.

    """
    # Retrieve value
    value = peek_key(schema=schema, schemas=schemas, key="default")
    if value is None:
        return None
    # Assemble schema
    resolved_schema: types.ColumnSchema = {
        "type": type_(schema=schema, schemas=schemas)
    }
    format_value = format_(schema=schema, schemas=schemas)
    max_length_value = max_length(schema=schema, schemas=schemas)
    if format_value is not None:
        resolved_schema["format"] = format_value
    if max_length_value is not None:
        resolved_schema["maxLength"] = max_length_value
    try:
        facades.jsonschema.validate(value, resolved_schema)
    except facades.jsonschema.ValidationError as exc:
        raise exceptions.MalformedSchemaError(
            "The default value does not conform to the schema. "
            f"The value is: {repr(value)}"
        ) from exc
    return value


def mixins(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.List[str]]:
    """
    Retrieve the x-mixins of the schema.

    Args:
        schema: The schema to get x-mixins from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-mixins or None.

    """
    key = "x-mixins"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None

    # Check value
    ext_prop_helper.get(source={key: value}, name=key)  # type: ignore

    # Transform string to list
    if isinstance(value, str):
        value = [value]

    # Check that each value is a valid dot-separated identifier
    def valid(mixin_value: str) -> bool:
        """Check whether a mixin value is valid."""
        components = mixin_value.split(".")
        if len(components) < 2:
            return False

        invalid_components = map(
            lambda component: not component.isidentifier(), components
        )
        return not any(invalid_components)

    values_valid = map(lambda mixin_value: (mixin_value, valid(mixin_value)), value)
    first_invalid_value = next(filter(lambda args: not args[1], values_valid), None)
    if first_invalid_value is not None:
        raise exceptions.MalformedExtensionPropertyError(
            f'mixin values must be a valid import path, "{first_invalid_value[0]}" is '
            "not"
        )

    return value


def dict_ignore(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[bool]:
    """
    Retrieve the x-dict-ignore property from a property schema.

    Raises MalformedSchemaError if the x-dict-ignore value is not a boolean.

    Args:
        schema: The schema to get the x-dict-ignore from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-dict-ignore value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-dict-ignore")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A x-dict-ignore value must be of type boolean."
        )
    return value


def peek_key(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    key: str,
    skip_ref: typing.Optional[str] = None,
) -> typing.Any:
    """
    Recursive type lookup.

    Raise MalformedSchemaError of a $ref value is seen again.

    Args:
        schema: The schema to look up the key in.
        schemas: All the schemas to resolve any $ref.
        key: The key to check for.
        seen_refs: All the $ref that have already been seen.
        skip_ref: The name of a reference to not follow.

    Returns:
        The key value (if found) or None.

    """
    return _peek_key(schema, schemas, key, set(), skip_ref=skip_ref)


def _peek_key(
    schema: types.Schema,
    schemas: types.Schemas,
    key: str,
    seen_refs: typing.Set[str],
    skip_ref: typing.Optional[str],
) -> typing.Any:
    """Implement peek_key."""
    # Check schema and schemas are dict
    if not isinstance(schema, dict):
        raise exceptions.MalformedSchemaError("The schema must be a dictionary.")
    if not isinstance(schemas, dict):
        raise exceptions.MalformedSchemaError("The schemas must be a dictionary.")

    # Base case, look for type key
    value = schema.get(key)
    if value is not None:
        return value

    # Recursive case, look for $ref
    ref_value = schema.get("$ref")
    if ref_value is not None:
        # Check that ref is string
        if not isinstance(ref_value, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")
        # Check for circular $ref
        if ref_value in seen_refs:
            raise exceptions.MalformedSchemaError("Circular reference detected.")
        seen_refs.add(ref_value)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref_value, schemas=schemas)
        if skip_ref is not None and ref_name == skip_ref:
            return None
        return _peek_key(ref_schema, schemas, key, seen_refs, skip_ref)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        # Check value of allOf
        if not isinstance(all_of, list):
            raise exceptions.MalformedSchemaError("The value of allOf must be a list.")

        for sub_schema in all_of:
            # Check value
            if not isinstance(sub_schema, dict):
                raise exceptions.MalformedSchemaError(
                    "The elements of allOf must be dictionaries."
                )

            value = _peek_key(sub_schema, schemas, key, seen_refs, skip_ref)
            if value is not None:
                return value

    # Base case, type or ref not found or no type in allOf
    return None


def prefer_local(
    *, get_value: PeekValue, schema: types.Schema, schemas: types.Schemas
) -> typing.Any:
    """
    Retrieve the value using a function preferably without having to follow a $ref.

    1. Check for allOf:
        if found, iterate over schemas in allOf and skip any that contain $ref and
            return the value returned by get_value if it is not None.
    2. Return output of get_value called on the schema.

    Args:
        get_value: The function that knows how to retrieve the value.
        schema: The schema to process.
        schemas: All the schemas.

    Returns:
        The value returned by get_value preferably without following any $ref.

    """
    all_of = schema.get("allOf")
    if all_of is not None:
        no_ref = filter(lambda sub_schema: sub_schema.get("$ref") is None, all_of)

        def map_to_value(sub_schema: types.Schema) -> typing.Any:
            """Use get_value to turn the schema into the value."""
            return get_value(schema=sub_schema, schemas=schemas)

        retrieved_values = map(map_to_value, no_ref)
        not_none_retrieved_values = filter(
            lambda value: value is not None, retrieved_values
        )
        retrieved_value = next(not_none_retrieved_values, None)
        if retrieved_value is not None:
            return retrieved_value
    return get_value(schema=schema, schemas=schemas)
