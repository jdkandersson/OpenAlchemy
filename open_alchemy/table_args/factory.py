"""Create table args such as Uniques and Index."""

import functools
import json
import os
import typing

from sqlalchemy import schema

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types

_DIRECTORY = os.path.dirname(__file__)
_PATHS = ("..", "helpers", "get_ext_prop")
_COMMON_SCHEMAS_FILE = os.path.join(_DIRECTORY, *_PATHS, "common-schemas.json")
(
    _resolver,  # pylint: disable=invalid-name
    (_COMMON_SCHEMAS,),
) = facades.jsonschema.resolver(_COMMON_SCHEMAS_FILE)


def _spec_to_schema_name(
    *, spec: types.AnyUnique, schema_names: typing.Optional[typing.List[str]] = None
) -> str:
    """
    Convert a specification to the name of the matched schema.

    Use the schema names defined in common-schemas.json to find the first matching
    schema.

    Args:
        spec: The specification to convert.
        schema_names: The names of the schemas to check.

    Returns:
        The name of the specification.

    """
    if schema_names is None:
        schema_names = list(_COMMON_SCHEMAS.keys())

    for name in schema_names:
        try:
            facades.jsonschema.validate(
                instance=spec, schema=_COMMON_SCHEMAS[name], resolver=_resolver
            )
            return name
        except facades.jsonschema.ValidationError:
            continue
    raise exceptions.SchemaNotFoundError("Specification did not match any schemas.")


def _handle_column_list(spec, property_name):
    """Convert ColumnList to a dictionary."""
    return {property_name: spec}


# Handling for column lists for unique constraints and index
_uq_handle_column_list = functools.partial(  # pylint: disable=invalid-name
    _handle_column_list, property_name="columns"
)
_ix_handle_column_list = functools.partial(  # pylint: disable=invalid-name
    _handle_column_list, property_name="expressions"
)

# Schema names for unique constraints and index
_SCHEMAS_FILE = os.path.join(_DIRECTORY, *_PATHS, "extension-schemas.json")
with open(_SCHEMAS_FILE) as in_file:
    _SCHEMAS = json.load(in_file)
_UNIQUE_SCHEMA_NAMES: typing.List[str] = list(
    map(
        lambda schema: schema["$ref"].split("/")[-1],
        _COMMON_SCHEMAS["CompositeUnique"]["oneOf"],
    )
)
_INDEX_SCHEMA_NAMES: typing.List[str] = list(
    map(
        lambda schema: schema["$ref"].split("/")[-1],
        _COMMON_SCHEMAS["CompositeIndex"]["oneOf"],
    )
)

# Unique and index name to conversion function
_UNIQUE_MAPPING: typing.Dict[str, typing.Callable[..., types.UniqueList]] = {
    "ColumnList": lambda spec: [_uq_handle_column_list(spec=spec)],
    "ColumnListList": lambda spec: list(map(_uq_handle_column_list, spec)),
    "Unique": lambda spec: [spec],
    "UniqueList": lambda spec: spec,
}
_INDEX_MAPPING: typing.Dict[str, typing.Callable[..., types.IndexList]] = {
    "ColumnList": lambda spec: [_ix_handle_column_list(spec=spec)],
    "ColumnListList": lambda spec: list(map(_ix_handle_column_list, spec)),
    "Index": lambda spec: [spec],
    "IndexList": lambda spec: spec,
}


def _map_unique(*, spec: types.AnyUnique) -> types.UniqueList:
    """
    Convert any unique constraint to UniqueList.

    Args:
        spec: The specification to convert.

    Returns:
        The UniqueList.

    """
    name = _spec_to_schema_name(spec=spec, schema_names=_UNIQUE_SCHEMA_NAMES)
    return _UNIQUE_MAPPING[name](spec)


def _map_index(*, spec: types.AnyIndex) -> types.IndexList:
    """
    Convert any composite index to IndexList.

    Args:
        spec: The specification to convert.

    Returns:
        The IndexList.

    """
    name = _spec_to_schema_name(spec=spec, schema_names=_INDEX_SCHEMA_NAMES)
    return _INDEX_MAPPING[name](spec)


def _construct_unique(spec: types.Unique) -> schema.UniqueConstraint:
    """
    Construct unique constraints.

    Args:
        spec: The definitions for the unique constraints.

    Returns:
        The unique constraints.

    """
    return schema.UniqueConstraint(*spec["columns"], name=spec.get("name"))


def _construct_index(spec: types.Index) -> schema.Index:
    """
    Construct composite index.

    Args:
        spec: The definitions for the composite index.

    Returns:
        The composite index.

    """
    return schema.Index(
        spec.get("name"), *spec["expressions"], unique=spec.get("unique")
    )


def unique_factory(
    *, spec: types.AnyUnique
) -> typing.Iterator[schema.UniqueConstraint]:
    """
    Generate unique constraints from specification.

    Args:
        spec: The specification to use.

    Returns:
        The unique constraints.

    """
    mapped_spec = _map_unique(spec=spec)
    return map(_construct_unique, mapped_spec)


def index_factory(*, spec: types.AnyUnique) -> typing.Iterator[schema.Index]:
    """
    Generate composite indexes from specification.

    Args:
        spec: The specification to use.

    Returns:
        The composite indexes.

    """
    mapped_spec = _map_index(spec=spec)
    return map(_construct_index, mapped_spec)
