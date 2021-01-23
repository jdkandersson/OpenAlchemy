"""
Cache for OpenAlchemy.

The name of the file is:
__open_alchemy_<sha256 of spec filename>_cache__

The structure of the file is:

{
    "hash": "<sha256 hash of the file contents>",
    "data": {
        "schemas": {
            "valid": true/false
        }
    }
}
"""

import hashlib
import json
import pathlib
import shutil

from . import exceptions


def calculate_hash(value: str) -> str:
    """Create hash of a value."""
    sha256 = hashlib.sha256()
    sha256.update(value.encode())
    return sha256.hexdigest()


def calculate_cache_path(path: pathlib.Path) -> pathlib.Path:
    """
    Calculate the name of the cache file.

    Args:
        path: The path to the spec file.

    Returns:
        The path to the cache file.

    """
    return path.parent / f"__open_alchemy_{calculate_hash(path.name)}_cache__"


_HASH_KEY = "hash"
_DATA_KEY = "data"
_DATA_SCHEMAS_KEY = "schemas"
_DATA_SCHEMAS_VALID_KEY = "valid"


def schemas_valid(filename: str) -> bool:
    """
    Calculate whether the cache indicates that the schemas in the file are valid.

    Algorithm:
    1. If the file does not exist, return False.
    2. If the file is actually a folder, return False.
    3. If the spec file is actually a folder, return False.
    4. If the spec file does not exist, return False.
    5. Calculate the hash of the spec file contents.
    6. Try to load the cache, if it fails or it is not a dictionary, return False.
    7. Try to retrieve the hash key, if it does not exist, return False.
    8. If the value of the hash key is different to the hash of the file, return False.
    9. Look for the data.schemas.valid key, if it does not exist, return False.
    12. If the value of data.schemas.valid is True return True, otherwise return False.

    Args:
        filename: The name of the OpenAPI specification file.

    Returns:
        Whether the cache indicates that the schemas in the file are valid.

    """
    path = pathlib.Path(filename)
    cache_path = calculate_cache_path(path)

    # Check that both file and cache exists and are files
    if (
        not path.exists()
        or not path.is_file()
        or not cache_path.exists()
        or not cache_path.is_file()
    ):
        return False

    file_hash = calculate_hash(path.read_text())

    try:
        cache = json.loads(cache_path.read_text())
    except json.JSONDecodeError:
        return False

    cache_valid = (
        isinstance(cache, dict)
        and _HASH_KEY in cache
        and _DATA_KEY in cache
        and isinstance(cache[_DATA_KEY], dict)
        and _DATA_SCHEMAS_KEY in cache[_DATA_KEY]
        and isinstance(cache[_DATA_KEY][_DATA_SCHEMAS_KEY], dict)
        and _DATA_SCHEMAS_VALID_KEY in cache[_DATA_KEY][_DATA_SCHEMAS_KEY]
    )
    if not cache_valid:
        return False

    cache_file_hash = cache[_HASH_KEY]
    if file_hash != cache_file_hash:
        return False

    return cache[_DATA_KEY][_DATA_SCHEMAS_KEY][_DATA_SCHEMAS_VALID_KEY] is True


def schemas_are_valid(filename: str) -> None:
    """
    Update the cache to indicate that the filename is valid.

    Algorithm:
    1. If the spec filename is actually a folder, raise a CacheError.
    2. If the spec filename does not exist, raise a CacheError.
    3. Calculate the hash of the spec file contents.
    4. If the chache is actually a folder, delete the folder.
    5. If the cache does not exist, create the cache.
    6. Read the contents of the cache. If it is not a dictionary, throw the contents
        away and create an empty dictionary.
    7. Create or update the hash key in the cache dictionary to be the calculated value.
    8. Look for the data key in the cache dictionary. If it does not exist or is not a
        dictionary, make it an empty dictionary.
    9. Look for the schemas key under data in the cache dictionary. If it does not exist
        or is not a dictionary, set it to be an empty dictionary.
    10. Create or update the valid key under data.schemas and set it to True.
    11. Write the dictionary to the file as JSON.

    Args:
        filename: The name of the spec file.

    """
    path = pathlib.Path(filename)
    if not path.exists():
        raise exceptions.CacheError(
            f"the spec file does not exists, filename={filename}"
        )
    if not path.is_file():
        raise exceptions.CacheError(f"the spec file is not a file, filename={filename}")
    file_hash = calculate_hash(path.read_text())

    cache_path = calculate_cache_path(path)
    if cache_path.exists() and not cache_path.is_file():
        shutil.rmtree(cache_path)
    if not cache_path.exists():
        cache_path.write_text("", encoding="utf-8")

    try:
        cache = json.loads(cache_path.read_text())
    except json.JSONDecodeError:
        cache = {}
    if not isinstance(cache, dict):
        cache = {}

    cache[_HASH_KEY] = file_hash

    if _DATA_KEY not in cache or not isinstance(cache[_DATA_KEY], dict):
        cache[_DATA_KEY] = {}
    cache_data = cache[_DATA_KEY]
    if _DATA_SCHEMAS_KEY not in cache_data or not isinstance(
        cache_data[_DATA_SCHEMAS_KEY], dict
    ):
        cache_data[_DATA_SCHEMAS_KEY] = {}
    cache_data_schemas = cache_data[_DATA_SCHEMAS_KEY]
    cache_data_schemas[_DATA_SCHEMAS_VALID_KEY] = True

    cache_path.write_text(json.dumps(cache), encoding="utf-8")
