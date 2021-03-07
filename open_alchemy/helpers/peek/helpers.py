"""Helpers for the peek functions."""

import typing

from open_alchemy import exceptions
from open_alchemy import types

from .. import ref as ref_helper


class PeekValue(types.Protocol):
    """Defines interface for peek functions."""

    def __call__(self, *, schema: types.Schema, schemas: types.Schemas) -> typing.Any:
        """Call signature for peek functions."""
        ...


def check_schema_schemas_dict(schema: types.Schema, schemas: types.Schemas) -> None:
    """Check that schema and schemas are dict."""
    # Check schema and schemas are dict
    if not isinstance(schema, dict):
        raise exceptions.MalformedSchemaError("The schema must be a dictionary.")
    if not isinstance(schemas, dict):
        raise exceptions.MalformedSchemaError("The schemas must be a dictionary.")


def check_ref_string(ref_value: typing.Any) -> str:
    """Check that value of $ref is string."""
    if not isinstance(ref_value, str):
        raise exceptions.MalformedSchemaError("The value of $ref must be a string.")
    return ref_value


def check_circular_ref(ref_value: str, seen_refs: typing.Set[str]) -> None:
    """Check whether ref has ever been seen."""
    if ref_value in seen_refs:
        raise exceptions.MalformedSchemaError("Circular reference detected.")
    seen_refs.add(ref_value)


def check_all_of_list(all_of: typing.Any) -> list:
    """Check that value of allOf is a list."""
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    return all_of


def check_sub_schema_dict(sub_schema: typing.Any) -> dict:
    """Check that a sub schema in an allOf is a dict."""
    if not isinstance(sub_schema, dict):
        raise exceptions.MalformedSchemaError(
            "The elements of allOf must be dictionaries."
        )
    return sub_schema


def peek_key(
    schema: types.Schema,
    schemas: types.Schemas,
    key: str,
    seen_refs: typing.Set[str],
    skip_ref: typing.Optional[str],
) -> typing.Any:
    """Execute peek_key."""
    check_schema_schemas_dict(schema, schemas)

    # Base case, look for type key
    keys = (
        [key.replace("x-", prefix) for prefix in types.KeyPrefixes]
        if key.startswith("x-")
        else [key]
    )
    value = next(filter(lambda value: value is not None, map(schema.get, keys)), None)
    if value is not None:
        return value

    # Recursive case, look for $ref
    ref_value = schema.get(types.OpenApiProperties.REF)
    if ref_value is not None:
        ref_value_str = check_ref_string(ref_value)
        check_circular_ref(ref_value_str, seen_refs)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref_value_str, schemas=schemas)
        if skip_ref is not None and ref_name == skip_ref:
            return None
        return peek_key(ref_schema, schemas, key, seen_refs, skip_ref)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        all_of_list = check_all_of_list(all_of)
        for sub_schema in all_of_list:
            sub_schema_dict = check_sub_schema_dict(sub_schema)
            value = peek_key(sub_schema_dict, schemas, key, seen_refs, skip_ref)
            if value is not None:
                return value

    # Base case, type or ref not found or no type in allOf
    return None


def prefer_local(
    get_value: PeekValue,
    schema: types.Schema,
    schemas: types.Schemas,
    seen_refs: typing.Set[str],
) -> typing.Any:
    """Execute prefer_local."""
    check_schema_schemas_dict(schema, schemas)

    # Handle $ref
    ref_value = schema.get(types.OpenApiProperties.REF)
    if ref_value is not None:
        ref_value_str = check_ref_string(ref_value)
        check_circular_ref(ref_value_str, seen_refs)

        _, ref_schema = ref_helper.get_ref(ref=ref_value_str, schemas=schemas)
        return prefer_local(get_value, ref_schema, schemas, seen_refs)

    # Handle allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        all_of_list = check_all_of_list(all_of)
        all_of_list_dict = map(check_sub_schema_dict, all_of_list)
        # Order putting any $ref last
        sorted_all_of = sorted(
            all_of_list_dict,
            key=lambda sub_schema: sub_schema.get(types.OpenApiProperties.REF)
            is not None,
        )

        def map_to_value(sub_schema: types.Schema) -> typing.Any:
            """Use get_value to turn the schema into the value."""
            return prefer_local(get_value, sub_schema, schemas, seen_refs)

        retrieved_values = map(map_to_value, sorted_all_of)
        not_none_retrieved_values = filter(
            lambda value: value is not None, retrieved_values
        )
        retrieved_value = next(not_none_retrieved_values, None)
        return retrieved_value

    return get_value(schema=schema, schemas=schemas)
