# """Tests for readOnly property validator pre-processor."""

# import pytest

# from open_alchemy.schemas.validation.property_ import read_only

# TESTS = [
#     pytest.param(
#         {"type": "not supported"},
#         {},
#         (False, "not supported type is not supported"),
#         id="type simple not supported",
#     ),
#     pytest.param(
#         {"type": "integer"},
#         {},
#         (True, None),
#         id="type integer",
#     ),
#     pytest.param(
#         {"type": "number"},
#         {},
#         (True, None),
#         id="type number",
#     ),
#     pytest.param(
#         {"type": "string"},
#         {},
#         (True, None),
#         id="type string",
#     ),
#     pytest.param(
#         {"type": "boolean"},
#         {},
#         (True, None),
#         id="type boolean",
#     ),
#     pytest.param(
#         {"type": "object"},
#         {},
#         (True, None),
#         id="type object no properties",
#     ),
#     pytest.param(
#         {"type": "object", "properties": True},
#         {},
#         (False, None),
#         id="type object properties not dict",
#     ),
# ]


# @pytest.mark.parametrize("schema, schemas, expected_result", TESTS)
# @pytest.mark.schemas
# def test_check(schema, schemas, expected_result):
#     """
#     GIVEN schemas, schema and the expected result
#     WHEN check is called with the schemas schema
#     THEN the expected result is returned.
#     """
#     # pylint: disable=assignment-from-no-return
#     returned_result = read_only.check(schemas, schema)

#     assert returned_result == expected_result
