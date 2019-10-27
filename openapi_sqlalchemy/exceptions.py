"""All custom exceptions that OpenAPI-SQLAlchemy can raise."""


class BaseError(Exception):
    """All exceptions derive at least from this exception."""


class MissingArgumentError(ValueError, BaseError):
    """Raised when a required argument was not passed."""


class SchemaNotFoundError(KeyError, BaseError):
    """Raised when a schema was not found in the schemas."""


class TypeMissingError(TypeError, BaseError):
    """Raised when a column schema does not have a type."""


class FeatureNotImplementedError(NotImplementedError, BaseError):
    """Raised when a requested feature has not been implemented yet."""


class MalformedSpecificationError(ValueError, BaseError):
    """Raised when an object specification is missing required properties."""


class MalformedSchemaError(ValueError, BaseError):
    """Raised when an object schema is missing required properties."""


class MalformedManyToOneRelationshipError(ValueError, BaseError):
    """Raised when a many to one relationship was not defined as expected."""


class MalformedExtensionPropertyError(ValueError, BaseError):
    """Raised when an extension property does not have the expected schema."""
