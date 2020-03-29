"""Tests for inheritance helpers."""

# import pytest

# from open_alchemy import exceptions
# from open_alchemy import helpers


# @pytest.mark.parametrize(
#     "schema, parent_name, schemas, exception",
#     [
#         ({}, "Parent", {}, exceptions.MalformedSchemaError),
#         (
#             {"$ref": "#/components/schemas/Parent"},
#             "Parent",
#             {},
#             exceptions.SchemaNotFoundError,
#         ),
#         (
#             {"$ref": "#/components/schemas/Parent"},
#             "Parent",
#             {"Parent": {"key": "value"}},
#             exceptions.MalformedSchemaError,
#         ),
#         (
#             {"allOf": []},
#             "Parent",
#             {"Parent": {"key": "value"}},
#             exceptions.MalformedSchemaError,
#         ),
#     ],
#     ids=[
#         "no $ref",
#         "$ref with parent that is not in schemas",
#         "$ref with parent that is not a table nor inherits",
#         "allOf no $ref",
#     ],
# )
# @pytest.mark.helper
# def test_check_parent_invalid(schema, parent_name, schemas, exception):
#     """
#     GIVEN schema, parent, schemas and expected exception
#     WHEN check_parent is called with the schema, parent and schemas
#     THEN the expected exception is raised.
#     """
#     with pytest.raises(exception):
#         helpers.inheritance.check_parent(
#             schema=schema, parent_name=parent_name, schemas=schemas
#         )
