"""All custom exceptions that OpenAlchemy can raise."""


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


class MalformedRelationshipError(ValueError, BaseError):
    """Raised when a relationship was not defined as expected."""


class MalformedExtensionPropertyError(ValueError, BaseError):
    """Raised when an extension property does not have the expected schema."""


class ModelAttributeError(AttributeError, BaseError):
    """Raised when a model lacks a required property."""


class InvalidModelInstanceError(ValueError, BaseError):
    """Raised when model instance object property does not implement to_dict."""


class MalformedModelDictionaryError(ValueError, BaseError):
    """Raised when an dictionary of a model does not satisfy the model schema."""
