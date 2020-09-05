"""Used to resolve schema references."""

import functools
import json
import os
import re
import typing
from urllib import error
from urllib import request

from open_alchemy import exceptions
from open_alchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


NameSchema = typing.Tuple[str, types.Schema]


def resolve(
    *,
    name: str,
    schema: types.Schema,
    schemas: types.Schemas,
    skip_name: typing.Optional[str] = None,
) -> NameSchema:
    """
    Resolve reference to another schema.

    Recursively resolves $ref until $ref key is no longer found. On each step, the name
    of the schema is recorded.

    Raises SchemaNotFoundError is a $ref resolution fails.
    Raise MalformedSchemaError of a $ref value is seen again.

    Args:
        name: The name of the schema from the last step.
        schema: The specification of the schema from the last step.
        schemas: Dictionary with all defined schemas used to resolve $ref.
        skip_name (optional): Skip the schema and return an empty schema instead.

    Returns:
        The first schema that no longer has the $ref key and the name of that schema.

    """
    return _resolve(name, schema, schemas, set(), skip_name)


def _resolve(
    name: str,
    schema: types.Schema,
    schemas: types.Schemas,
    seen_refs: typing.Set[str],
    skip_name: typing.Optional[str],
) -> NameSchema:
    """Implement resolve."""
    # Checking whether schema is a reference schema
    ref = schema.get("$ref")
    if ref is None:
        return name, schema
    # Check that ref is string
    if not isinstance(ref, str):
        raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

    # Check for circular $ref
    if ref in seen_refs:
        raise exceptions.MalformedSchemaError("Circular reference chain detected.")
    seen_refs.add(ref)

    ref_name, ref_schema = get_ref(ref=ref, schemas=schemas)

    # Check if schema should be skipped
    if ref_name == skip_name:
        return name, {}

    return _resolve(ref_name, ref_schema, schemas, seen_refs, skip_name)


def get_ref(*, ref: str, schemas: types.Schemas) -> NameSchema:
    """
    Get the schema referenced by ref.

    Raises SchemaNotFoundError if a $ref resolution fails.

    Args:
        ref: The reference to the schema.
        schemas: The schemas to use to resolve the ref.

    Returns:
        The schema referenced by ref.

    """
    # Check for remote $ref
    if not ref.startswith("#"):
        return get_remote_ref(ref=ref)

    # Checking value of $ref
    match = _REF_PATTER.match(ref)
    if not match:
        raise exceptions.SchemaNotFoundError(
            f"{ref} format incorrect, expected #/components/schemas/<SchemaName>"
        )

    # Retrieving new schema
    ref_name = match.group(1)
    ref_schema = schemas.get(ref_name)
    if ref_schema is None:
        raise exceptions.SchemaNotFoundError(f"{ref_name} was not found in schemas.")

    return ref_name, ref_schema


# URL $ref regex
_URL_REF_PATTERN = re.compile(r"^(https?:)\/\/", re.IGNORECASE)


def _norm_context(*, context: str) -> str:
    """
    Normalize the path and case of a context.

    Args:
        context: The context to normalize.

    Returns:
        The normalized context.

    """
    if _URL_REF_PATTERN.search(context) is not None:
        return context
    norm_context = os.path.normpath(context)
    return os.path.normcase(norm_context)


def _separate_context_path(*, ref: str) -> typing.Tuple[str, str]:
    """
    Separate the context and path of a reference.

    Raise MalformedSchemaError if the reference does not contain #.

    Args:
        ref: The reference to separate.

    Returns:
        The context and path to the schema as a tuple.

    """
    try:
        ref_context, ref_schema = ref.split("#")
    except ValueError as exc:
        raise exceptions.MalformedSchemaError(
            f"A reference must contain exactly one #. Actual reference: {ref}"
        ) from exc
    return ref_context, ref_schema


# Regex for capturing the hostname and path from a URL
_HOSTNAME_REF_PATTERM = re.compile(r"^(https?:\/\/.*?)(\/.*)$", re.IGNORECASE)


def _add_remote_context(*, context: str, ref: str) -> str:
    """
    Add remote context to any $ref within a schema retrieved from a remote reference.

    There are 5 cases:
    1. The $ref value starts with # in which case the context is prepended.
    2. The $ref starts with a filename in which case only the directory portion of the
        context is prepended.
    3. The $ref starts with a relative path and ends with a file in which case the
        directory portion of the context is prepended and merged so that the shortest
        possible relative path is used.
    4. The $ref starts with a HTTP protocol, in which case no changes are made.
    5. The $ref starts with // in which case the HTTP protocol of the context is
        prepended.

    Raise SchemaNotFoundError if the $ref starts with // when the context does not start
        with a HTTP protocol.

    After the paths are merged the following operations are done:
    1. a normalized relative path is calculated (eg. turning ./dir1/../dir2 to ./dir2)
        and
    2. the case is normalized.

    Args:
        context: The context of the document from which the schema was retrieved which
            is the relative path to the file on the system from the base OpenAPI
            specification.
        ref: The value of a $ref within the schema.

    Returns:
        The $ref value with the context of the document included.

    """
    # Check for URL reference
    url_match = _URL_REF_PATTERN.search(ref)
    if url_match is not None:
        return ref
    if ref.startswith("//"):
        context_protocol = _URL_REF_PATTERN.search(context)
        if context_protocol is None:
            raise exceptions.SchemaNotFoundError(
                "A reference starting with // is only valid from within a document "
                f"loaded from a URL. The reference is {ref}, the location of the "
                f"document with the reference is {context}."
            )
        return f"{context_protocol.group(1)}{ref}"

    # Handle reference within document
    ref_context, ref_schema = _separate_context_path(ref=ref)
    if not ref_context:
        return f"{context}{ref}"

    # Break context into components
    # Default where context is not a URL
    context_hostname = ""
    context_path = context
    # Gather components if the context is a URL
    hostname_match = _HOSTNAME_REF_PATTERM.search(context)
    if hostname_match is not None:
        context_hostname = hostname_match.group(1)
        context_path = hostname_match.group(2)
    context_path_head, _ = os.path.split(context_path)

    # Handle reference outside document
    new_ref_context_path = os.path.join(context_path_head, ref_context)
    norm_new_ref_context_path = _norm_context(context=new_ref_context_path)
    return f"{context_hostname}{norm_new_ref_context_path}#{ref_schema}"


def _handle_match(match: typing.Match, *, context: str) -> str:
    """
    Map a match to the updated value.

    Args:
        match: The match to the regular expression for the reference.
        context: The context to use to update the reference.

    Returns:
        The updated reference.

    """
    ref = match.group(1)
    mapped_ref = _add_remote_context(context=context, ref=ref)
    return match.group(0).replace(ref, mapped_ref)


# Pattern used to look for any $ref after converting the schema to JSON
_REF_VALUE_PATTERN = re.compile(r'"\$ref": "(.*?)"')


def _map_remote_schema_ref(*, schema: types.Schema, context: str) -> types.Schema:
    """
    Update any $ref within the schema with the remote context.

    Serialize the schema, look for $ref and update value to include context.

    Args:
        schema: The schema to update.
        context: The context of the schema.

    Returns:
        The schema with any $ref mapped to include the context.

    """
    # Define context for mapping
    handle_match_context = functools.partial(_handle_match, context=context)

    str_schema = json.dumps(schema)
    mapped_str_schema = _REF_VALUE_PATTERN.sub(handle_match_context, str_schema)
    mapped_schema = json.loads(mapped_str_schema)
    return mapped_schema


class _RemoteSchemaStore:
    """Store remote schemas in memory to speed up use."""

    _schemas: typing.Dict[str, types.Schemas]
    spec_context: typing.Optional[str]

    def __init__(self) -> None:
        """Construct."""
        self._schemas = {}
        self.spec_context = None

    def reset(self):
        """Reset the state of the schema store."""
        self._schemas = {}
        self.spec_context = None

    def get_schemas(self, *, context: str) -> types.Schema:
        """
        Retrieve the schemas for a context.

        Raise MissingArgumentError if the context for the original OpenAPI specification
            has not been set.
        Raise SchemaNotFoundError if the context doesn't exist or is not a json nor yaml
            file.

        Args:
            context: The path, relative to the original OpenAPI specification, for the
                file containing the schemas.

        Returns:
            The schemas.

        """
        # Check whether the context is already loaded
        if context in self._schemas:
            return self._schemas[context]

        if self.spec_context is None:
            raise exceptions.MissingArgumentError(
                "Cannot find the file containing the remote reference, either "
                "initialize OpenAlchemy with init_json or init_yaml or pass the path "
                "to the OpenAPI specification to OpenAlchemy."
            )

        # Check for json, yaml or yml file extension
        _, extension = os.path.splitext(context)
        extension = extension.lower()
        if extension not in {".json", ".yaml", ".yml"}:
            raise exceptions.SchemaNotFoundError(
                "The remote context is not a JSON nor YAML file. The path is: "
                f"{context}"
            )

        # Get context manager with file
        try:
            if _URL_REF_PATTERN.search(context) is not None:
                file_cm = request.urlopen(context)
            else:
                spec_dir = os.path.dirname(self.spec_context)
                remote_spec_filename = os.path.join(spec_dir, context)
                file_cm = open(remote_spec_filename)
        except (FileNotFoundError, error.HTTPError) as exc:
            raise exceptions.SchemaNotFoundError(
                "The file with the remote reference was not found. The path is: "
                f"{context}"
            ) from exc

        # Calculate location of schemas
        with file_cm as in_file:
            if extension == ".json":
                try:
                    schemas = json.load(in_file)
                except json.JSONDecodeError as exc:
                    raise exceptions.SchemaNotFoundError(
                        "The remote reference file is not valid JSON. The path "
                        f"is: {context}"
                    ) from exc
            else:
                # Import as needed to make yaml optional
                import yaml  # pylint: disable=import-outside-toplevel

                try:
                    schemas = yaml.safe_load(in_file)
                except yaml.scanner.ScannerError as exc:
                    raise exceptions.SchemaNotFoundError(
                        "The remote reference file is not valid YAML. The path "
                        f"is: {context}"
                    ) from exc

        # Store for faster future retrieval
        self._schemas[context] = schemas
        return schemas


_remote_schema_store = _RemoteSchemaStore()  # pylint: disable=invalid-name


def set_context(*, path: str) -> None:
    """
    Set the context for the initial OpenAPI specification.

    Args:
        path: The path to the OpenAPI specification

    """
    _remote_schema_store.spec_context = path


def _retrieve_schema(*, schemas: types.Schemas, path: str) -> NameSchema:
    """
    Retrieve schema at a path from schemas.

    Raise SchemaNotFoundError if the schema is not found at the path.

    Args:
        schemas: All the schemas.
        path: The location to retrieve the schema from.

    Returns:
        The schema at the path from the schemas.

    """
    # Strip leading /
    if path.startswith("/"):
        path = path[1:]

    # Get the first directory/file as the head and the remaining path as the tail
    path_components = path.split("/", 1)

    try:
        # Base case, no tail
        if len(path_components) == 1:
            return path_components[0], schemas[path_components[0]]
        # Recursive case, call again with path tail
        return _retrieve_schema(
            schemas=schemas[path_components[0]], path=path_components[1]
        )
    except KeyError as exc:
        raise exceptions.SchemaNotFoundError(
            f"The schema was not found in the remote schemas. Path subsection: {path}"
        ) from exc


def get_remote_ref(*, ref: str) -> NameSchema:
    """
    Retrieve remote schema based on reference.

    Args:
        ref: The reference to the remote schema.

    Returns:
        The remote schema.

    """
    context, path = _separate_context_path(ref=ref)
    context = _norm_context(context=context)
    schemas = _remote_schema_store.get_schemas(context=context)
    name, schema = _retrieve_schema(schemas=schemas, path=path)
    schema = _map_remote_schema_ref(schema=schema, context=context)
    return name, schema
