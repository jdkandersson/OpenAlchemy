"""Retrieve artifacts for backref property."""

import typing

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types

# import copy


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
    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    assert type_ in OPEN_API_TO_SUB_TYPE
    sub_type = OPEN_API_TO_SUB_TYPE[type_]

    return types.BackrefPropertyArtifacts(
        type_=helpers.property_.type_.Type.BACKREF,
        sub_type=sub_type,
        schema={},
        properties=[],
    )
