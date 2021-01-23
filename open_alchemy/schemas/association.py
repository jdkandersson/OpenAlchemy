"""Pre-process schemas by adding any association tables as a schema to schemas."""

import typing

from .. import types
from ..helpers import inheritance
from ..helpers import peek
from .helpers import association as association_helper
from .helpers import iterate


def _assert_is_string(value: typing.Any) -> str:
    """Assert that a value is a string."""
    assert isinstance(value, str)
    return value


def _get_association_tablenames(
    *,
    association_schemas: typing.List[types.TNameSchema],
) -> typing.Set[str]:
    """
    Get the tablenames of the associations.

    Args:
        association_schemas: All the association schemas.

    Returns:
        A set of tablenames from the associations.

    """
    tablenames = map(
        lambda association: peek.tablename(schema=association.schema, schemas={}),
        association_schemas,
    )
    str_tablenames = map(_assert_is_string, tablenames)
    return set(str_tablenames)


class _TParentAllNames(typing.NamedTuple):
    """The name of the parent schema and all schemas with the same tablename."""

    parent_name: str
    all_names: typing.List[str]


_TTablenameParentAllNames = typing.Dict[str, _TParentAllNames]


def _get_tablename_schema_names(
    *, schemas: types.Schemas, tablenames: typing.Set[str]
) -> _TTablenameParentAllNames:
    """
    Get a mapping of tablenames to all schema names with that tablename.

    The algorithm is:
    1. Get a mapping of the tablename to the parent schema name by skipping any single
        table inheritance children.
    2. Get a list of schema names and tablenames and filter for those that are in the
        mapping.
    3. Combine any schema names with the same tablename and lookup the parent schema
        name.

    Args:
        schemas: All defines schemas.
        tablenames: All tablenames to filter for.

    Returns:
        A mapping of association tablenames to all schema names using that tablename
        and the parent schema name of a tablename.

    """
    # Get mapping of tablename to parent schema name
    constructables = iterate.constructable(schemas=schemas)
    not_single_inheritance_constructables = filter(
        lambda args: inheritance.calculate_type(schema=args[1], schemas=schemas)
        != inheritance.Type.SINGLE_TABLE,
        constructables,
    )
    tablename_parent_name_map = dict(
        map(
            lambda args: (
                peek.prefer_local(
                    get_value=peek.tablename, schema=args[1], schemas=schemas
                ),
                args[0],
            ),
            not_single_inheritance_constructables,
        )
    )

    # Get a list of schema names and tablenames which appear in the mapping
    constructables = iterate.constructable(schemas=schemas)
    name_tablenames = map(
        lambda args: (
            args[0],
            peek.prefer_local(
                get_value=peek.tablename, schema=args[1], schemas=schemas
            ),
        ),
        constructables,
    )
    filtered_name_tablenames = filter(
        lambda args: args[1] in tablenames, name_tablenames
    )

    mapping: _TTablenameParentAllNames = {}
    for name, tablename in filtered_name_tablenames:
        if tablename not in mapping:
            mapping[tablename] = _TParentAllNames(
                parent_name=tablename_parent_name_map[tablename], all_names=[]
            )
        mapping[tablename].all_names.append(name)

    return mapping


class _TParentNameForeignKeys(typing.NamedTuple):
    """The name of the parent schema and all foreign keys on the same tablename."""

    parent_name: str
    foreign_keys: typing.Set[str]


_TTablenameForeignKeys = typing.Dict[str, _TParentNameForeignKeys]


def _get_tablename_foreign_keys(
    tablename_parent_all_names: _TTablenameParentAllNames, schemas: types.Schemas
) -> _TTablenameForeignKeys:
    """
    Get a mapping of tablename to foreign keys defined on that tablename.

    Algorithm:
    1. Combine all the schema names on the same tablename using allOf and get all the
        properties on that tablename.
    2. Retrieve the value of x-foreign-key on each property and filter for those that
        are strings.
    3. Combine into a mapping of tablename against the foreign keys and parent name.

    Args:
        tablename_parent_all_names: Mapping of tablename to schema names.
        schemas: All defined schemas.

    Returns:
        Mapping of tablename to the parent schema and all foreign keys defined on that
        tablename.

    """
    # Get all the properties on a tablename
    tablename_schemas = map(
        lambda args: (
            args[0],
            {
                "allOf": [
                    {types.OpenApiProperties.REF: f"#/components/schemas/{name}"}
                    for name in args[1].all_names
                ]
            },
        ),
        tablename_parent_all_names.items(),
    )
    tablename_properties = map(
        lambda args: (
            args[0],
            iterate.properties_items(schema=args[1], schemas=schemas),
        ),
        tablename_schemas,
    )

    # Get all the foreign keys of the properties on the tablename
    tablename_foreign_keys = map(
        lambda args: (
            args[0],
            map(
                lambda property_: peek.prefer_local(
                    get_value=peek.foreign_key,
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

    # Combine the tablename against the parent name and foreign keys
    return dict(
        map(
            lambda args: (
                args[0],
                _TParentNameForeignKeys(
                    parent_name=tablename_parent_all_names[args[0]].parent_name,
                    foreign_keys=args[1],
                ),
            ),
            tablename_foreign_key_set,
        )
    )


def _combine_defined_expected_schema(
    parent_name_foreign_keys: _TParentNameForeignKeys,
    expected_schema: types.TNameSchema,
    schemas: types.Schemas,
) -> types.TNameSchema:
    """
    Combine defined and expected association schema.

    Algorithm:
    1. For the expected schema:
        a. Remove required array
        b. Filter the properties where their foreign is already defined
    2. Combine the expected schema in an allOf with the defined schema parent name.
    3. Change the name to the parent name.

    Args:
        parent_name_foreign_keys: The parent name and defined foreign keys of the
            defined association schema.
        expected_schema: The expected schema.

    Returns:
        The combined expected and defined schema.

    """
    expected_schema_value = expected_schema.schema
    del expected_schema_value[types.OpenApiProperties.REQUIRED]
    expected_schema_value[types.OpenApiProperties.PROPERTIES] = {
        property_[0]: property_[1]
        for property_ in expected_schema_value[
            types.OpenApiProperties.PROPERTIES
        ].items()
        if peek.foreign_key(schema=property_[1], schemas={})
        not in parent_name_foreign_keys.foreign_keys
    }
    return types.TNameSchema(
        name=parent_name_foreign_keys.parent_name,
        schema={
            "allOf": [
                expected_schema_value,
                schemas[parent_name_foreign_keys.parent_name],
            ]
        },
    )


def _combine_defined_expected_schemas(
    *, association_schemas: typing.List[types.TNameSchema], schemas: types.Schemas
) -> typing.Iterator[types.TNameSchema]:
    """
    Combine all association schemas with any defined schemas.

    Args:
        association_schemas: All expected association schemas.
        schemas: All defined schemas.

    Returns:
        The association schemas merged with any existing schemas.

    """
    association_tablenames = _get_association_tablenames(
        association_schemas=association_schemas
    )
    tablename_schema_names = _get_tablename_schema_names(
        schemas=schemas, tablenames=association_tablenames
    )
    tablename_foreign_keys = _get_tablename_foreign_keys(
        tablename_parent_all_names=tablename_schema_names, schemas=schemas
    )

    for association_schema in association_schemas:
        association_tablename = peek.tablename(
            schema=association_schema.schema, schemas={}
        )
        if association_tablename not in tablename_foreign_keys:
            yield association_schema
            continue

        yield _combine_defined_expected_schema(
            tablename_foreign_keys[association_tablename], association_schema, schemas
        )


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
    association_properties = association_helper.get_association_property_iterator(
        schemas=schemas
    )
    association_schemas = list(
        map(
            lambda args: association_helper.calculate_schema(
                property_schema=args.property.schema,
                parent_schema=args.parent.schema,
                schemas=schemas,
            ),
            association_properties,
        )
    )
    combined_association_schemas = _combine_defined_expected_schemas(
        association_schemas=association_schemas, schemas=schemas
    )
    for association in combined_association_schemas:
        schemas[association.name] = association.schema
