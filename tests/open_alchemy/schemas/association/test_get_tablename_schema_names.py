"""Tests for _get_tablename_schema_names association schemas function."""

import pytest

from open_alchemy.schemas import association


class TestGetTablenameSchemaNames:
    """Tests for _get_tablename_schema_names."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param({}, set(), {}, id="empty"),
        pytest.param({"Schema1": {}}, set(), {}, id="single not constructable"),
        pytest.param(
            {"Schema1": {"x-tablename": "table 1"}},
            set("table 2"),
            {},
            id="single miss",
        ),
        pytest.param(
            {"Schema1": {"x-tablename": "table 1"}},
            {"table 1"},
            {"table 1": ("Schema1", ["Schema1"])},
            id="single hit",
        ),
        pytest.param(
            {
                "Schema1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-inherits": True},
                    ]
                },
                "RefSchema": {"x-tablename": "table 1"},
            },
            {"table 1"},
            {"table 1": ("RefSchema", ["Schema1", "RefSchema"])},
            id="single hit $ref first",
        ),
        pytest.param(
            {
                "RefSchema": {"x-tablename": "table 1"},
                "Schema1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-inherits": True},
                    ]
                },
            },
            {"table 1"},
            {"table 1": ("RefSchema", ["RefSchema", "Schema1"])},
            id="single hit $ref second",
        ),
        pytest.param(
            {"Schema1": {"allOf": [{"x-tablename": "table 1"}]}},
            {"table 1"},
            {"table 1": ("Schema1", ["Schema1"])},
            id="single hit allOf",
        ),
        pytest.param(
            {
                "Schema1": {
                    "allOf": [
                        {"x-tablename": "table 1"},
                        {"$ref": "#/components/schemas/RefSchema"},
                    ]
                },
                "RefSchema": {"x-tablename": "ref_table"},
            },
            {"table 1"},
            {"table 1": ("Schema1", ["Schema1"])},
            id="single hit allOf local $ref local first",
        ),
        pytest.param(
            {
                "Schema1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-tablename": "table 1"},
                    ]
                },
                "RefSchema": {"x-tablename": "ref_table"},
            },
            {"table 1"},
            {"table 1": ("Schema1", ["Schema1"])},
            id="single hit allOf local $ref $ref first",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
            },
            set(),
            {},
            id="multiple miss",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
            },
            {"table 1"},
            {"table 1": ("Schema1", ["Schema1"])},
            id="multiple first hit",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
            },
            {"table 2"},
            {"table 2": ("Schema2", ["Schema2"])},
            id="multiple second hit",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
            },
            {"table 1", "table 2"},
            {"table 1": ("Schema1", ["Schema1"]), "table 2": ("Schema2", ["Schema2"])},
            id="multiple all hit",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 1"},
            },
            {"table 1"},
            {"table 1": ("Schema2", ["Schema1", "Schema2"])},
            id="multiple same tablename",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
                "Schema3": {"x-tablename": "table 3"},
            },
            {"table 1", "table 2", "table 3"},
            {
                "table 1": ("Schema1", ["Schema1"]),
                "table 2": ("Schema2", ["Schema2"]),
                "table 3": ("Schema3", ["Schema3"]),
            },
            id="many different tablename",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 1"},
                "Schema3": {"x-tablename": "table 3"},
            },
            {"table 1", "table 2", "table 3"},
            {
                "table 1": ("Schema2", ["Schema1", "Schema2"]),
                "table 3": ("Schema3", ["Schema3"]),
            },
            id="many different first middle same tablename",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
                "Schema3": {"x-tablename": "table 1"},
            },
            {"table 1", "table 2", "table 3"},
            {
                "table 1": ("Schema3", ["Schema1", "Schema3"]),
                "table 2": ("Schema2", ["Schema2"]),
            },
            id="many first last same tablename",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
                "Schema3": {"x-tablename": "table 2"},
            },
            {"table 1", "table 2", "table 3"},
            {
                "table 1": ("Schema1", ["Schema1"]),
                "table 2": ("Schema3", ["Schema2", "Schema3"]),
            },
            id="many middle last same tablename",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 1"},
                "Schema3": {"x-tablename": "table 1"},
            },
            {"table 1", "table 2", "table 3"},
            {"table 1": ("Schema3", ["Schema1", "Schema2", "Schema3"])},
            id="many all same tablename",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("schemas, tablenames, expected_mapping", TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(schemas, tablenames, expected_mapping):
        """
        GIVEN schemas, tablenames and expected mappng
        WHEN _get_tablename_schema_names is called with the schemas and tablenames
        THEN the expected mapping is returned.
        """
        returned_mapping = association._get_tablename_schema_names(
            schemas=schemas, tablenames=tablenames
        )

        assert returned_mapping == expected_mapping
