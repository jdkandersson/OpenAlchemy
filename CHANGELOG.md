# Release Notes

## Version 1.2.0 - 2020-06-08

- Remove several bugs from the generated models file and integrate with `sqlalchemy-stubs`.
- Ring fence `black` dependency.
- add support for `__str__` and `__repr__` for model instances.

## Version 1.1.1 - 2020-05-17

- Add support for `readOnly`.
- Fix bug where TypedDIct types for `binary`, `date` and `date-time` string formats mapped to the incorrect python types.
- Fix bug where `to_dict` and `to_str` returned `null` for values that are not required and not nullable.

## Version 1.1.0 - 2020-04-05

- Add section of documentation for each example.
- Add support for keyword arguments for relationships used to define relationship arguments not specifically handled by an extension property.
- Add support for kwargs at the model, column and foreign key level.
- Add support for single and joined table inheritance.

## Version 1.0.0 - 2020-03-21

- Add support for remote references to a file at a URL.
- Add support for default values.
- Add check for whether the value of an extension property is null.

## Version 0.14.0 - 2020-02-21

- Add support for remote references to another file on the file system.

## Version 0.13.0 - 2020-02-16

- Ring fence SQLAlchemy dependency to a facade and integration tests.
- Add tests for examples.
- Add `from_str` and `to_str` to complement `from_dict` and `to_dict` for de-serializing and serializing from JSON.
- Ring fence jsonschema dependency into a facade.
- Add description from OpenAPI specification into the models file.

## Version 0.12.1 - 2020-01-12

- Fix bug where auto generating models file meant that multiple classes with the same name were registered with the base.

## Version 0.12.0 - 2020-01-04

- Fix bug where format and maxLength was not considered for the foreign key constructed for an object reference.
- Refactor object reference handling to be easier to understand.
- Add checking whether the column is automatically generated to determining the type of a column.
- Remove typing_extensions dependency for Python version 3.8 and later.
- Add support for `nullable` for object references.
- Add type hints for `\_\_init\_\_` and `from_dict`.
- Add example for alembic interoperability.

## Version 0.11.0 - 2019-12-29

- Add support for `password`
- Add support for `binary`
- Add support for `byte`
- Add support for `date`
- Move SQLAlchemy relationship construction behind facade
- Move schema calculations into separate files
- Refactor handling array references to reduce scope of individual tests and make them easier to understand
- Add optional parameter that can be used to generate a models file for IDE auto complete and type hinting
- Add `from_dict` and `to_dict` to the type models file
- Add SQLAlchemy information to models file
- Add back references to models file

## Version 0.10.4 - 2019-12-18

- Fix bug where some static files where not included in the distribution.

## Version 0.10.1 - 2019-12-15

- Refactor column handler to first check the schema, then gather the required artifacts for column construction and then construct the column.
- Add support for DateTime.

## Version 0.10.0 - 2019-11-23
_Beta release_

- Add check for whether foreign key for relationship is already constructed before automatically constructing it.
- Add support for returning parent properties in the child `to_dict` call using `readOnly` properties.
- Add support for many to many relationships.

## Version 0.9.1 - 2019-11-11

- Fix bug where some static files where not included in the distribution.

## Version 0.9.0 - 2019-11-10

- Add `from_dict` and `to_dict` functions to all models that are used to construct a model from a dictionary and to convert a model instance to a dictionary, respectively.
- Add `x-foreign-key-column` extension property to define a custom foreign key constraint for many to one relationships.
- Add `x-composite-unique` extension property at the object level to construct unique constraints with multiple columns.
- Add `x-composite-index` extension property at the object level to construct indexes with multiple columns.
- Add support for one to one relationships.
- Fix bug where `allOf` merging would only return the properties of the last object instead of merging the properties.
- Add support for one to many relationships.

## Version 0.8.0 - 2019-11-03
- Add less verbose initialisation with `init_yaml` and `init_json`.
- Remove need for separate models file by exposing `Base` and constructed models at `open_alchemy.models`.
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
