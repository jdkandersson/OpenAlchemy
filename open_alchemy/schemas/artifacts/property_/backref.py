"""Retrieve artifacts for backref property."""

import copy
import typing

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types

OPEN_API_TO_SUB_TYPE: typing.Dict[
    str,
    typing.Union[
        oa_types.Literal[types.BackrefSubType.OBJECT],
        oa_types.Literal[types.BackrefSubType.ARRAY],
    ],
] = {
    "object": types.BackrefSubType.OBJECT,
    "array": types.BackrefSubType.ARRAY,
}


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema
) -> types.BackrefPropertyArtifacts:
    """
    Retrieve the artifacts for a backref property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the backref property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    schema = copy.deepcopy(
        oa_helpers.schema.prepare_deep(schema=schema, schemas=schemas)
    )

    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    assert type_ in OPEN_API_TO_SUB_TYPE
    sub_type = OPEN_API_TO_SUB_TYPE[type_]

    description = oa_helpers.peek.description(schema=schema, schemas=schemas)

    # Get property names
    properties_items: typing.Iterable[typing.Tuple[str, typing.Any]]
    if sub_type == types.BackrefSubType.OBJECT:  # noqa: E721
        properties_items = helpers.iterate.properties_items(
            schema=schema, schemas=schemas
        )
    else:
        items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
        assert items_schema is not None
        properties_items = helpers.iterate.properties_items(
            schema=items_schema, schemas=schemas
        )
    properties_names = map(lambda args: args[0], properties_items)

    return types.BackrefPropertyArtifacts(
        type=helpers.property_.type_.Type.BACKREF,
        description=description,
        sub_type=sub_type,
        schema=schema,
        required=None,
        properties=list(properties_names),
    )
