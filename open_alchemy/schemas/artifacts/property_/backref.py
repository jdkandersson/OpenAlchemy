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
        typing.Literal[types.BackrefSubType.OBJECT],
        typing.Literal[types.BackrefSubType.ARRAY],
    ],
] = {
    "object": types.BackrefSubType.OBJECT,
    "array": types.BackrefSubType.ARRAY,
}


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema
) -> types.BackrefPropertyArtifacts:
    """
    Retrieve the artifacts for a simple property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the simple property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    schema = copy.deepcopy(
        oa_helpers.schema.prepare_deep(schema=schema, schemas=schemas)
    )

    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    assert type_ in OPEN_API_TO_SUB_TYPE
    sub_type = OPEN_API_TO_SUB_TYPE[type_]

    properties_items: typing.Iterable[typing.Tuple[str, typing.Any]]
    if sub_type == types.BackrefSubType.OBJECT:
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
        type_=helpers.property_.type_.Type.BACKREF,
        sub_type=sub_type,
        schema=schema,
        required=False,
        properties=list(properties_names),
    )
