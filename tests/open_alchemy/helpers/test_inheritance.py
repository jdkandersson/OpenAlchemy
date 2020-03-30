"""Tests for inheritance helpers."""

# import pytest

# from open_alchemy import exceptions
# from open_alchemy import helpers


# @pytest.mark.parametrize(
#     "name, parent_name, schemas, exception",
#     [
#         ("Child", "Parent", {}, exceptions.SchemaNotFoundError),
#         ("Child", "Parent", {"Child": {}}, exceptions.MalformedSchemaError),
#         (
#             "Child",
#             "Parent",
#             {"Child": {"$ref": "#/components/schemas/Parent"}},
#             exceptions.MalformedSchemaError,
#         ),
#         (
#             "Child",
#             "Parent",
#             {
#                 "Child": {"$ref": "#/components/schemas/Parent"},
#                 "Parent": {"key": "value"},
#             },
#             exceptions.MalformedSchemaError,
#         ),
#         (
#             "Child",
#             "Parent",
#             {"Child": {"allOf": []}, "Parent": {"key": "value"}},
#             exceptions.MalformedSchemaError,
#         ),
#     ],
#     ids=[
#         "child that is not in schemas",
#         "no $ref",
#         "$ref with parent that is not in schemas",
#         "$ref with parent that is not a table nor inherits",
#         "allOf no $ref",
#     ],
# )
# @pytest.mark.helper
# def test_check_parent_invalid(name, parent_name, schemas, exception):
#     """
#     GIVEN child and parent name, schemas and expected exception
#     WHEN check_parent is called with the names and schemas
#     THEN the expected exception is raised.
#     """
#     with pytest.raises(exception):
#         helpers.inheritance.check_parent(
#             name=name, parent_name=parent_name, schemas=schemas
#         )
