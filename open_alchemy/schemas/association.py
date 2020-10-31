"""Pre-process schemas by adding any association tables as a schema to schemas."""

import typing

from .. import helpers as oa_helpers
from .. import types
from . import helpers


def _assert_is_string(value: typing.Any) -> str:
    """Assert that a value is a string."""
    assert isinstance(value, str)
    return value


def _get_association_tablenames(
    *, association_schemas: typing.List[types.TNameSchema]
) -> typing.Set[str]:
    """
    Get the tablenames of the associations.

    Args:
        association_schemas: All the association schemas.

    Returns:
        A set of tablenames from the associations.

    """
    tablenames = map(
        lambda association: oa_helpers.peek.tablename(
            schema=association.schema, schemas={}
        ),
        association_schemas,
    )
    str_tablenames = map(_assert_is_string, tablenames)
    return set(str_tablenames)


_TTablenameNames = typing.Dict[str, typing.List[str]]


def _get_tablename_schema_names(
    *, schemas: types.Schemas, tablenames: typing.Set[str]
) -> _TTablenameNames:
    """
    Get a mapping of tablenames to all schema names with that tablename.

    Args:
        schemas: All defines schemas.
        tablenames: All tablenames to filter for.

    Returns:
        A mapping of association tablenames to all schema names using that tablename.

    """
    constructables = helpers.iterate.constructable(schemas=schemas)
    name_tablenames = map(
        lambda args: (
            args[0],
            oa_helpers.peek.prefer_local(
                get_value=oa_helpers.peek.tablename, schema=args[1], schemas=schemas
            ),
        ),
        constructables,
    )
    filtered_name_tablenames = filter(
        lambda args: args[1] in tablenames, name_tablenames
    )

    mapping: _TTablenameNames = {}
    for name, tablename in filtered_name_tablenames:
        if tablename not in mapping:
            mapping[tablename] = []
        mapping[tablename].append(name)

    return mapping


_TTablenameForeignKeys = typing.Dict[str, typing.Set[str]]


def _get_tablename_foreign_keys(
    *, tablename_names: _TTablenameNames, schemas: types.Schemas
) -> _TTablenameForeignKeys:
    """
    Get a mapping of tablename to foreign keys defined on that tablename.

    Args:
        tablename_names: Mapping of tablename to schema names.
        schemas: All defined schemas.

    Returns:
        Mapping of tablename to all foreign keys defined on that tablename.

    """
    tablename_schemas = map(
        lambda args: (
            args[0],
            {"allOf": [{"$ref": f"#/components/schemas/{name}"} for name in args[1]]},
        ),
        tablename_names.items(),
    )
    tablename_properties = map(
        lambda args: (
            args[0],
            helpers.iterate.properties_items(schema=args[1], schemas=schemas),
        ),
        tablename_schemas,
    )
    tablename_foreign_keys = map(
        lambda args: (
            args[0],
            map(
                lambda property_: oa_helpers.peek.prefer_local(
                    get_value=oa_helpers.peek.foreign_key,
                    schema=property_[1],
                    schemas=schemas,
                ),
                args[1],
            ),
        ),
        tablename_properties,
    )
    tablename_str_foreign_keys = map(
        lambda args: (
            args[0],
            filter(lambda foreign_key: isinstance(foreign_key, str), args[1]),
        ),
        tablename_foreign_keys,
    )
    tablename_foreign_key_set = map(
        lambda args: (args[0], set(args[1])), tablename_str_foreign_keys
    )
    return dict(tablename_foreign_key_set)


def process(*, schemas: types.Schemas) -> None:
    """
    Pre-process the schemas to add association schemas as necessary.

    Algorithm:
    1. Iterate over all schemas and their properties retaining the parent schema and the
        schemas in the context and staying within the model properties only
    2. Filter for properties that (1) are relationships and (2) are many-to-many
        relationships
    3. Convert the property schema to an association schema
    4. Add them to the schemas

    Args:
        schemas: The schemas to process.

    """
    association_properties = helpers.association.get_association_property_iterator(
        schemas=schemas
    )
    association_schemas = list(
        map(
            lambda args: helpers.association.calculate_schema(
                property_schema=args.property.schema,
                parent_schema=args.parent.schema,
                schemas=schemas,
            ),
            association_properties,
        )
    )
    for association in association_schemas:
        schemas[association.name] = association.schema
