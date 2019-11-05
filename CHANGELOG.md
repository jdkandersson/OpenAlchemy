# Release Notes

## Version _unreleased_

- Add _from_dict_ and _to_dict_ functions to all models that are used to construct a model from a dictionary and to convert a model instance to a dictionary, respectively.

## Version 0.8.0 - 2019-11-03
- Add less verbose initialisation with _init_yaml_ and _init_json_.
- Remove need for separate models file by exposing _Base_ and constructed models at _open_alchemy.models_.
- Update name from OpenAPI-SQLAlchemy to OpenAlchemy

## Version 0.7.0 - 2019-10-27
- Add support for Python 3.6.
- Add connexion example application.
- Fixed bug where referencing a schema which uses allOf in many to one relationships does not merge the allOf statement.
- Fixed bug where a type hint that is not always exported from SQLAlchemy may cause an no member error.
- Add schema checking for extension properties.

## Version 0.6.3 - 2019-10-19
- Add support for backref for many to one relationships.
- Refactor to remove reference resolving decorator.
- Add integration tests for major features.

## Version 0.6.2 - 2019-10-19
- Add support for python 3.8.

## Version 0.6.1 - 2019-10-19
- Update name from openapi-SQLAlchemy to OpenAPI-SQLAlchemy. All urls are expected to keep working.

## Version 0.6.0 - 2019-10-6
- Add support for `allOf` for models.

## Version 0.5.0 - 2019-09-29
- Refactor column factory to use fewer decorators.
- Change exceptions to include the schema name.
- Add support for `$ref` for models.

## Version 0.4.0 - 2019-09-21
- Add support for `allOf` for columns.

## Version 0.3.0 - 2019-09-08
- Add support for `autoincrement`.
- Add support for `$ref` for columns referencing other table objects.
- Add documentation

## Version 0.2.0 - 2019-08-25
- Add support for `$ref` for columns.

## Version 0.1.1 - 2019-08-18
- Move typing-extensions development to package dependency.

## Version 0.1.0 - 2019-08-18
- Initial release
- Add support for `integer` columns.
- Add support for `boolean` columns.
- Add support for `number` columns.
- Add support for `string` columns.
