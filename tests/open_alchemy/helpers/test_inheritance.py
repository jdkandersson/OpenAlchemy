# """Tests for inheritance helpers."""

# import pytest

# from open_alchemy import exceptions
# from open_alchemy import helpers


# @pytest.mark.parametrize(
#     "schemas, exception",
#     [
#         ({}, exceptions.SchemaNotFoundError),
#         ({"Child": {}}, exceptions.MalformedSchemaError),
#         ({"Child": {"allOf": []}}, exceptions.MalformedSchemaError),
#         (
#             {"Child": {"$ref": "#/components/schemas/Parent"}},
#             exceptions.MalformedSchemaError,
#         ),
#         (
#             {"Child": {"allOf": [{"$ref": "#/components/schemas/Parent"}]}},
#             exceptions.MalformedSchemaError,
#         ),
#     ],
#     ids=[
#         "child that is not in schemas",
#         "no $ref",
#         "allOf no $ref",
#         "$ref with parent that is not in schemas",
#         "allOf $ref with parent that is not in schemas",
#     ],
# )
# @pytest.mark.helper
# def test_check_parent_invalid(schemas, exception):
#     """
#     GIVEN child and parent name, schemas and expected exception
#     WHEN check_parent is called with the names and schemas
#     THEN the expected exception is raised.
#     """
#     name = "Child"
#     parent_name = "Parent"

#     with pytest.raises(exception):
#         helpers.inheritance.check_parent(
#             name=name, parent_name=parent_name, schemas=schemas
#         )


# @pytest.mark.parametrize(
#     "schemas, expected_result",
#     [
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {"x-tablename": "table 1"}},
#             },
#             True,
#         ),
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {"$ref": "#/components/schemas/Grandparent"}},
#                 {"Grandparent": {"x-tablename": "table 1"}},
#             },
#             False,
#         ),
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {"x-inherits": True}},
#             },
#             True,
#         ),
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {"x-inherits": False}},
#             },
#             False,
#         ),
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {"x-inherits": "Grandparent"}},
#             },
#             True,
#         ),
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {}},
#             },
#             False,
#         ),
#         (
#             {
#                 {"Child": {"$ref": "#/components/schemas/Parent"}},
#                 {"Parent": {"allOf": []}},
#             },
#             False,
#         ),
#     ],
#     ids=[
#         "base name match plain x-tablename",
#         "base name match plain $ref to x-tablename",
#         "base name match plain x-inherits bool true",
#         "base name match plain x-inherits bool false",
#         "base name match plain x-inherits string",
#         "base name match plain missing",
#         "base name match allOf empty",
#         "base name match allOf $ref only",
#         "base name match allOf x-tablename",
#         "base name match allOf x-inherits bool true",
#         "base name match allOf x-inherits bool false",
#         "base name match allOf x-inherits string",
#         "base name match allOf missing",
#         "base name match $ref with x-tablename",
#         "base name match allOf $ref with x-tablename",
#         "single $ref to valid",
#         "multiple $ref to valid",
#         "allOf empty",
#         "allOf single valid",
#         "allOf single invalid",
#         "allOf multiple invalid",
#         "allOf multiple some valid",
#         "allOf multiple all valid",
#     ],
# )
