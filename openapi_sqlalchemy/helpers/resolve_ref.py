"""Used to resolve schema references."""

from openapi_sqlalchemy.types import SchemaType


class MissingArgumentError(ValueError):
    """Raised when a required argument was not passed."""


class SchemaNotFoundError(KeyError):
    """Raised when a schema was not found in the schemas."""


def resolve_ref(*, schema: SchemaType):
    """Resolve $ref schemas to the underlying schema."""
    return schema
