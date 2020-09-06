"""All custom exceptions that OpenAlchemy can raise."""


class BaseError(Exception):
    """All exceptions derive at least from this exception."""

    def __init__(self, message, **kwargs):
        """Construct."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(message)

    def __str__(self):
        """Convert exception to string."""
        kwargs_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"{super().__str__()} {kwargs_str}"


class MissingArgumentError(BaseError, ValueError):
    """Raised when a required argument was not passed."""


class SchemaNotFoundError(BaseError, KeyError):
    """Raised when a schema was not found in the schemas."""


class TypeMissingError(TypeError, BaseError):
    """Raised when a column schema does not have a type."""


class FeatureNotImplementedError(BaseError, NotImplementedError):
    """Raised when a requested feature has not been implemented yet."""


class MalformedSpecificationError(BaseError, ValueError):
    """Raised when an object specification is missing required properties."""


class MalformedSchemaError(BaseError, ValueError):
    """Raised when an object schema is missing required properties."""


class MalformedRelationshipError(BaseError, ValueError):
    """Raised when a relationship was not defined as expected."""


class MalformedExtensionPropertyError(BaseError, ValueError):
    """Raised when an extension property does not have the expected schema."""


class ModelAttributeError(BaseError, AttributeError):
    """Raised when a model lacks a required property."""


class InvalidModelInstanceError(BaseError, ValueError):
    """Raised when model instance object property does not implement to_dict."""


class InvalidInstanceError(BaseError, ValueError):
    """Raised when the an instance of a schema does not conform to the schema."""


class MalformedModelDictionaryError(BaseError, ValueError):
    """Raised when an dictionary of a model does not satisfy the model schema."""


class InheritanceError(BaseError):
    """Raised when an error related to inheritance occurs."""


class BuildError(BaseError):
    """Raised when an error related to build occurs."""
