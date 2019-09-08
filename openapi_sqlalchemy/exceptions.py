"""All custom exceptions that openapi-SQLAlchemy can raise."""


class MissingArgumentError(ValueError):
    """Raised when a required argument was not passed."""


class SchemaNotFoundError(KeyError):
    """Raised when a schema was not found in the schemas."""


class TypeMissingError(TypeError):
    """Raised when a column schema does not have a type."""


class FeatureNotImplementedError(NotImplementedError):
    """Raised when a requested feature has not been implemented yet."""


class MalformedSpecificationError(ValueError):
    """Raised when an object specification is missing required properties."""


class MalformedSchemaError(ValueError):
    """Raised when an object schema is missing required properties."""
