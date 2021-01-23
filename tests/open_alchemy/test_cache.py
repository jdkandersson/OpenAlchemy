"""Tests for the cache."""

import json
import pathlib

import pytest

from open_alchemy import cache
from open_alchemy import exceptions


@pytest.mark.parametrize(
    "spec_path, expected_cache_path",
    [
        pytest.param(
            pathlib.Path("some.file"),
            pathlib.Path(f"__open_alchemy_{cache.calculate_hash('some.file')}_cache__"),
            id="json file",
        ),
        pytest.param(
            pathlib.Path("parent/some.file"),
            pathlib.Path(
                f"parent/__open_alchemy_{cache.calculate_hash('some.file')}_cache__"
            ),
            id="file in subfolder",
        ),
    ],
)
@pytest.mark.cache
def test_calculate_cache_path(spec_path, expected_cache_path):
    """
    GIVEN spec path
    WHEN calculate_cache_path is called with the spec path
    THEN the expected path is returned.
    """
    returned_path = cache.calculate_cache_path(spec_path)

    assert str(returned_path) == str(expected_cache_path)


@pytest.mark.cache
def test_schemas_valid_spec_file_not_exists(tmpdir):
    """
    GIVEN spec file that does not exist and cache with contents
    WHEN schemas_valid is called with the filename
    THEN False is returned.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_file = path_tmpdir / "spec.json"
    cache_file = path_tmpdir / "__open_alchemy_spec_json_cache__"
    cache_file.write_text(
        "cache 1",
        encoding="utf-8",
    )

    returned_result = cache.schemas_valid(str(spec_file))

    assert returned_result is False


@pytest.mark.cache
def test_schemas_valid_spec_file_is_folder(tmpdir):
    """
    GIVEN spec file that is actually a folder and cache with contents
    WHEN schemas_valid is called with the filename
    THEN False is returned.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_file = path_tmpdir / "spec.json"
    spec_file.mkdir()
    cache_file = path_tmpdir / "__open_alchemy_spec_json_cache__"
    cache_file.write_text(
        "cache 1",
        encoding="utf-8",
    )

    returned_result = cache.schemas_valid(str(spec_file))

    assert returned_result is False


@pytest.mark.cache
def test_schemas_valid_cache_file_missing(tmpdir):
    """
    GIVEN spec file with contents and cache that does not exist
    WHEN schemas_valid is called with the filename
    THEN False is returned.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_file = path_tmpdir / "spec.json"
    spec_file.write_text("spec 1", encoding="utf-8")

    returned_result = cache.schemas_valid(str(spec_file))

    assert returned_result is False


@pytest.mark.cache
def test_schemas_valid_cache_is_folder(tmpdir):
    """
    GIVEN spec file with contents and cache that is a folder
    WHEN schemas_valid is called with the filename
    THEN False is returned.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_file = path_tmpdir / "spec.json"
    spec_file.write_text("spec 1", encoding="utf-8")
    cache_file = path_tmpdir / "__open_alchemy_spec_json_cache__"
    cache_file.mkdir()

    returned_result = cache.schemas_valid(str(spec_file))

    assert returned_result is False


@pytest.mark.parametrize(
    "spec_contents, cache_contents, expected_result",
    [
        pytest.param("spec 1", "", False, id="empty"),
        pytest.param("spec 1", "invalid JSON", False, id="not json"),
        pytest.param("spec 1", "true", False, id="not dictionary"),
        pytest.param("spec 1", json.dumps({}), False, id="empty dictionary"),
        pytest.param(
            "spec 1",
            json.dumps({"data": {"schemas": {"valid": True}}}),
            False,
            id="hash missing data schemas valid True",
        ),
        pytest.param(
            "spec 1",
            json.dumps({"hash": None, "data": {"schemas": {"valid": True}}}),
            False,
            id="hash not string data schemas valid True",
        ),
        pytest.param(
            "spec 1",
            json.dumps(
                {
                    "hash": cache.calculate_hash("spec 2"),
                    "data": {"schemas": {"valid": True}},
                }
            ),
            False,
            id="hash different data schemas valid True",
        ),
        pytest.param(
            "spec 1",
            json.dumps({"hash": cache.calculate_hash("spec 1")}),
            False,
            id="hash same  data missing",
        ),
        pytest.param(
            "spec 1",
            json.dumps({"hash": cache.calculate_hash("spec 1"), "data": None}),
            False,
            id="hash same  data not dict",
        ),
        pytest.param(
            "spec 1",
            json.dumps({"hash": cache.calculate_hash("spec 1"), "data": {}}),
            False,
            id="hash same  data schemas missing",
        ),
        pytest.param(
            "spec 1",
            json.dumps(
                {"hash": cache.calculate_hash("spec 1"), "data": {"schemas": None}}
            ),
            False,
            id="hash same  data schemas not dict",
        ),
        pytest.param(
            "spec 1",
            json.dumps(
                {"hash": cache.calculate_hash("spec 1"), "data": {"schemas": {}}}
            ),
            False,
            id="hash same  data schemas valid missing",
        ),
        pytest.param(
            "spec 1",
            json.dumps(
                {
                    "hash": cache.calculate_hash("spec 1"),
                    "data": {"schemas": {"valid": None}},
                }
            ),
            False,
            id="hash same  data schemas valid not boolean",
        ),
        pytest.param(
            "spec 1",
            json.dumps(
                {
                    "hash": cache.calculate_hash("spec 1"),
                    "data": {"schemas": {"valid": False}},
                }
            ),
            False,
            id="hash same  data schemas valid False",
        ),
        pytest.param(
            "spec 1",
            json.dumps(
                {
                    "hash": cache.calculate_hash("spec 1"),
                    "data": {"schemas": {"valid": True}},
                }
            ),
            True,
            id="hash same data schemas valid True",
        ),
    ],
)
@pytest.mark.cache
def test_schemas_valid(tmpdir, spec_contents, cache_contents, expected_result):
    """
    GIVEN spec file with contents and cache with contents
    WHEN schemas_valid is called with the filename
    THEN the expected result is returned.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_filename = "spec.json"
    spec_file = path_tmpdir / spec_filename
    spec_file.write_text(spec_contents, encoding="utf-8")
    cache_file = (
        path_tmpdir / f"__open_alchemy_{cache.calculate_hash(spec_filename)}_cache__"
    )
    cache_file.write_text(
        cache_contents,
        encoding="utf-8",
    )

    returned_result = cache.schemas_valid(str(spec_file))

    assert returned_result == expected_result


@pytest.mark.cache
def test_schemas_are_valid_spec_missing(tmpdir):
    """
    GIVEN spec is missing
    WHEN schemas_are_valid is called with the spec filename
    THEN CacheError is raised.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_filename = "spec.json"
    spec_file = path_tmpdir / spec_filename

    with pytest.raises(exceptions.CacheError):
        cache.schemas_are_valid(str(spec_file))


@pytest.mark.cache
def test_schemas_are_valid_spec_not_file(tmpdir):
    """
    GIVEN spec is actually a folder
    WHEN schemas_are_valid is called with the spec filename
    THEN CacheError is raised.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_filename = "spec.json"
    spec_file = path_tmpdir / spec_filename
    spec_file.mkdir()

    with pytest.raises(exceptions.CacheError):
        cache.schemas_are_valid(str(spec_file))


@pytest.mark.cache
def test_schemas_are_valid(tmpdir):
    """
    GIVEN spec in a file and the cache is actually a folder
    WHEN schemas_are_valid is called with the spec filename
    THEN schemas_valid returns True if it is called afterwards.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_filename = "spec.json"
    spec_file = path_tmpdir / spec_filename
    spec_file.write_text("spec 1", encoding="utf-8")
    cache_file = (
        path_tmpdir / f"__open_alchemy_{cache.calculate_hash(spec_filename)}_cache__"
    )
    cache_file.mkdir()
    cache_sub_file = cache_file / "some.file"
    cache_sub_file.write_text("some contents")

    cache.schemas_are_valid(str(spec_file))

    assert cache.schemas_valid(str(spec_file)) is True


@pytest.mark.cache
def test_schemas_are_valid_cache_folder(tmpdir):
    """
    GIVEN spec in a file
    WHEN schemas_are_valid is called with the spec filename
    THEN schemas_valid returns True if it is called afterwards.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_filename = "spec.json"
    spec_file = path_tmpdir / spec_filename
    spec_file.write_text("spec 1", encoding="utf-8")

    cache.schemas_are_valid(str(spec_file))

    assert cache.schemas_valid(str(spec_file)) is True


@pytest.mark.parametrize(
    "cache_contents",
    [
        pytest.param("", id="empty"),
        pytest.param("not valid JSON", id="invalid JSON"),
        pytest.param(json.dumps(True), id="not dict"),
        pytest.param(json.dumps({}), id="empty dict"),
        pytest.param(json.dumps({"hash": None}), id="hash exists"),
        pytest.param(json.dumps({"data": None}), id="data exists not dict"),
        pytest.param(json.dumps({"data": {}}), id="data exists empty"),
        pytest.param(
            json.dumps({"data": {"schemas": None}}), id="data schema not dict"
        ),
        pytest.param(json.dumps({"data": {"schemas": {}}}), id="data schema empty"),
        pytest.param(
            json.dumps({"data": {"schemas": {"valid": None}}}),
            id="data schema valid not boolean",
        ),
        pytest.param(
            json.dumps({"data": {"schemas": {"valid": False}}}),
            id="data schema valid False",
        ),
        pytest.param(
            json.dumps({"data": {"schemas": {"valid": True}}}),
            id="data schema valid True",
        ),
    ],
)
@pytest.mark.cache
def test_schemas_are_valid_cache_exists(tmpdir, cache_contents):
    """
    GIVEN spec in a file
    WHEN schemas_are_valid is called with the spec filename
    THEN schemas_valid returns True if it is called afterwards.
    """
    path_tmpdir = pathlib.Path(tmpdir)
    spec_filename = "spec.json"
    spec_file = path_tmpdir / spec_filename
    spec_file.write_text("spec 1", encoding="utf-8")
    cache_file = (
        path_tmpdir / f"__open_alchemy_{cache.calculate_hash(spec_filename)}_cache__"
    )
    cache_file.write_text(
        cache_contents,
        encoding="utf-8",
    )

    cache.schemas_are_valid(str(spec_file))

    assert cache.schemas_valid(str(spec_file)) is True
