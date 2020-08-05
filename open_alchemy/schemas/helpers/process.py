"""Helpers to process schemas."""

import itertools
import typing

from ... import types
from . import iterate


class Artifacts(typing.NamedTuple):
    """The return value of _calculate_schema."""

    schema_name: str
    property_name: str
    property_schema: types.Schema


ArtifactsIter = typing.Iterator[Artifacts]
ArtifactsGroupedIter = typing.Iterator[typing.Tuple[str, ArtifactsIter]]
SchemaIter = typing.Iterable[typing.Tuple[str, types.Schema]]
GetSchemaArtifacts = typing.Callable[[types.Schemas, str, types.Schema], ArtifactsIter]


def get_artifacts(
    *, schemas: types.Schemas, get_schema_artifacts: GetSchemaArtifacts
) -> ArtifactsIter:
    """
    Get all back reference information from the schemas.

    Takes all schemas, retrieves all constructable schemas, for each schema retrieves
    all back references and returns an iterable with all the captured back references.

    Args:
        schemas: The schemas to process.

    Returns:
        All backreference information.

    """
    # Retrieve all constructable schemas
    constructables = iterate.constructable(schemas=schemas)
    # Retrieve all backrefs
    backrefs_iters = map(
        lambda args: get_schema_artifacts(schemas, *args), constructables
    )
    # Unpack nested iterators
    return itertools.chain(*backrefs_iters)
