"""Define all the models with x-tablename properties."""

from open_alchemy import helpers
from open_alchemy import types


def define_all(*, model_factory: types.ModelFactory, schemas: types.Schemas) -> None:
    """
    Define all the models with x-tablename properties.

    Args:
        model_factory: Factory used to construct models.
        schemas: The schemas from which to define all.

    """
    for name, schema in schemas.items():
        if helpers.peek.tablename(schema=schema, schemas=schemas) is None:
            continue
        model_factory(name=name)
