# Release Notes

## Version _next_

- Add support for _date_
- Move SQLAlchemy relationship construction behind facade
- Move schema calculations into separate files

## Version 0.10.4 - 2019-12-18

- Fix bug where some static files where not included in the distribution.

## Version 0.10.1 - 2019-12-15

- Refactor column handler to first check the schema, then gather the required artifacts for column construction and then construct the column.
- Add support for DateTime.

## Version 0.10.0 - 2019-11-23
_Beta release_

- Add check for whether foreign key for relationship is already constructed before automatically constructing it.
- Add support for returning parent properties in the child _to_dict_ call using _readOnly_ properties.
- Add support for many to many relationships.

## Version 0.9.1 - 2019-11-11

- Fix bug where some static files where not included in the distribution.

## Version 0.9.0 - 2019-11-10

- Add _from_dict_ and _to_dict_ functions to all models that are used to construct a model from a dictionary and to convert a model instance to a dictionary, respectively.
- Add _x-foreign-key-column_ extension property to define a custom foreign key constraint for many to one relationships.
- Add _x-composite-unique_ extension property at the object level to construct unique constraints with multiple columns.
- Add _x-composite-index_ extension property at the object level to construct indexes with multiple columns.
- Add support for one to one relationships.
- Fix bug where _allOf_ merging would only return the properties of the last object instead of merging the properties.
- Add support for one to many relationships.

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
- Add support for _allOf_ for models.

## Version 0.5.0 - 2019-09-29
- Refactor column factory to use fewer decorators.
- Change exceptions to include the schema name.
- Add support for _$ref_ for models.

## Version 0.4.0 - 2019-09-21
- Add support for _allOf_ for columns.

## Version 0.3.0 - 2019-09-08
- Add support for _autoincrement_.
- Add support for _$ref_ for columns referencing other table objects.
- Add documentation

## Version 0.2.0 - 2019-08-25
- Add support for _$ref_ for columns.

## Version 0.1.1 - 2019-08-18
- Move typing-extensions development to package dependency.

## Version 0.1.0 - 2019-08-18
- Initial release
- Add support for _integer_ columns.
- Add support for _boolean_ columns.
- Add support for _number_ columns.
- Add support for _string_ columns.
