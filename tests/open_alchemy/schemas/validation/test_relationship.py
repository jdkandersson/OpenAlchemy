"""Tests for relationship validation."""

# import pytest

# from open_alchemy.schemas.validation import relationship


# @pytest.mark.parametrize(
#     "schema, schemas, expected_result",
#     [
#         pytest.param({}, {}, (False, "type missing"), id="no type"),
#         pytest.param(
#             {"type": "not relationship"},
#             {},
#             (False, "type not an object nor array"),
#             id="not object nor array type",
#         ),
#         pytest.param(
#             {"type": "object"},
#             {},
#             (False, "not a reference to another object"),
#             id="not object no $ref",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {"RefSchema": {"type": "object"}},
#             (False, "referenced schema not constructable"),
#             id="object $ref not constructable",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one $ref",
#         ),
#         pytest.param(
#             {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one allOf",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "nullable": True,
#                 }
#             },
#             (True, None),
#             id="many to one nullable $ref",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "nullable": True,
#                 }
#             },
#             (False, "value of nullable must be a boolean"),
#             id="many to one nullable $ref not bool",
#         ),
#         pytest.param(
#             {"allOf": [{"$ref": "#/components/schemas/RefSchema"},
#  {"nullable": True}]},
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one nullable allOf",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"nullable": True},
#                     {"nullable": False},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "multiple nullable defined in allOf"),
#             id="many to one nullable allOf multiple",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "x-backref": "schema",
#                 }
#             },
#             (True, None),
#             id="many to one backref $ref",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "x-backref": True,
#                 }
#             },
#             (False, "value of x-backref must be a string"),
#             id="many to one backref $ref not string",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-backref": "schema"},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one backref allOf",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-backref": "schema"},
#                     {"x-backref": "ref_schema"},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "multiple x-backref defined in allOf"),
#             id="many to one backref allOf multiple",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "x-foreign-key-column": "id",
#                 }
#             },
#             (True, None),
#             id="many to one foreign-key-column $ref",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "x-foreign-key-column": True,
#                 }
#             },
#             (False, "value of x-foreign-key-column must be a string"),
#             id="many to one foreign-key-column $ref not string",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-foreign-key-column": "id"},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one foreign-key-column allOf",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-foreign-key-column": "id"},
#                     {"x-foreign-key-column": "name"},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, "multiple x-foreign-key-column defined in allOf"),
#             id="many to one foreign-key-column allOf multiple",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-kwargs": {"key": "value"}},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one allOf kwargs",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-kwargs": {"key_1": "value 1"}},
#                     {"x-kwargs": {"key_2": "value 2"}},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "multiple x-kwargs defined in allOf"),
#             id="many to one allOf kwargs multiple",
#         ),
#         pytest.param(
#             {"allOf": [{"$ref": "#/components/schemas/RefSchema"},
# {"x-kwargs": True}]},
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "value of x-kwargs must be a dictionary"),
#             id="many to one allOf kwargs not dict",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-kwargs": {"backref": "schema"}},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "x-kwargs may not contain the backref key"),
#             id="many to one allOf kwargs has backref",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-kwargs": {"secondary": "schema"}},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "x-kwargs may not contain the secondary key"),
#             id="many to one allOf kwargs has secondary",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "x-uselist": True,
#                 }
#             },
#             (True, None),
#             id="many to one $ref uselist",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-uselist": True},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="many to one allOf uselist",
#         ),
#         pytest.param(
#             {"$ref": "#/components/schemas/RefSchema"},
#             {
#                 "RefSchema": {
#                     "type": "object",
#                     "x-tablename": "ref_schema",
#                     "x-uselist": False,
#                     "x-backref": "schema",
#                 }
#             },
#             (True, None),
#             id="one to one $ref",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-uselist": False, "x-backref": "schema"},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (True, None),
#             id="one to one allOf",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-uselist": False},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "a one-to-one relationship must define a back reference"),
#             id="one to one allOf no backref",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-uselist": "False", "x-backref": "schema"},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "value of x-uselist must be a boolean"),
#             id="one to one allOf uselist not boolean",
#         ),
#         pytest.param(
#             {
#                 "allOf": [
#                     {"$ref": "#/components/schemas/RefSchema"},
#                     {"x-uselist": False, "x-backref": "schema"},
#                     {"x-uselist": True},
#                 ]
#             },
#             {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
#             (False, "multiple x-uselist defined in allOf"),
#             id="one to one allOf multiple uselist",
#         ),
#         pytest.param(id="array no items"),
#         pytest.param(id="array items no type"),
#         pytest.param(id="array items type not object"),
#         pytest.param(id="array items no $ref"),
#         pytest.param(id="array items no $ref not constructable"),
#         pytest.param(id="one to many $ref"),
#         pytest.param(id="$ref one to many $ref"),
#         pytest.param(id="allOf one to many $ref"),
#         pytest.param(id="one to many allOf"),
#         pytest.param(id="one to many allOf nullable False"),
#         pytest.param(id="one to many allOf nullable True"),
#         pytest.param(id="one to many backref on root"),
#         pytest.param(id="one to many backref $ref"),
#         pytest.param(id="one to many backref $ref not string"),
#         pytest.param(id="one to many backref allOf"),
#         pytest.param(id="one to many backref allOf multiple"),
#         pytest.param(id="one to many foreign-key-column on root"),
#         pytest.param(id="one to many foreign-key-column $ref"),
#         pytest.param(id="one to many foreign-key-column $ref not string"),
#         pytest.param(id="one to many foreign-key-column allOf"),
#         pytest.param(id="one to many foreign-key-column allOf multiple"),
#         pytest.param(id="one to many kwargs on root"),
#         pytest.param(id="one to many allOf kwargs"),
#         pytest.param(id="one to many allOf kwargs multiple"),
#         pytest.param(id="one to many allOf kwargs key not string"),
#         pytest.param(id="one to many allOf kwargs has backref"),
#         pytest.param(id="one to many allOf kwargs has secondary"),
#         pytest.param(id="one to many $ref uselist"),
#         pytest.param(id="one to many allOf uselist"),
#         pytest.param(id="many to many $ref"),
#         pytest.param(id="many to many $ref secondary not string"),
#         pytest.param(id="many to many allOf"),
#         pytest.param(id="many to many allOf nullable False"),
#         pytest.param(id="many to many allOf nullable True"),
#         pytest.param(id="many to many allOf multiple secondary"),
#         pytest.param(id="many to many backref on root"),
#         pytest.param(id="many to many backref $ref"),
#         pytest.param(id="many to many backref $ref not string"),
#         pytest.param(id="many to many backref allOf"),
#         pytest.param(id="many to many backref allOf multiple"),
#         pytest.param(id="many to many kwargs on root"),
#         pytest.param(id="many to many allOf kwargs"),
#         pytest.param(id="many to many allOf kwargs multiple"),
#         pytest.param(id="many to many allOf kwargs key not string"),
#         pytest.param(id="many to many allOf kwargs has backref"),
#         pytest.param(id="many to many allOf kwargs has secondary"),
#         pytest.param(id="many to many $ref uselist"),
#         pytest.param(id="many to many allOf uselist"),
#         pytest.param(id="one to many foreign-key-column on root"),
#         pytest.param(id="one to many foreign-key-column $ref"),
#         pytest.param(id="one to many foreign-key-column allOf"),
#     ],
# )
# @pytest.mark.schemas
# def test_check(schema, schemas, expected_result):
#     """
#     GIVEN schema, schemas and expected result
#     WHEN check is called with the schemas and schema
#     THEN the expected result is returned.
#     """
