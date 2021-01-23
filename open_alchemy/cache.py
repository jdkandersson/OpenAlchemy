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
