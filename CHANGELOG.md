# Release Notes

## Version _next_

- Remove `define_all` parameter for `init_model_factory`, `init_json` and
  `init_yaml`. OpenAlchemy now behaves as though `define_all` is set to
  `True`. _This means that a pure model reference (a schema with only the
  `$ref` key) can no longer be used to change the name of a model._
- Fix bug where the association table defined for `many-to-many` relationships
  did not make the foreign key columns referencing the two sides of the
  relationship primary keys. _This may require a database migration if alembic
  was used to generate the database schema._
- Change the association table to no longer be noted on the models based on
  the `x-secondary` value and instead be noted based on converting the
  `x-secondary` value from snake_case to PascalCase. Name clashes are avoided
  by pre-pending `Autogen` as many times as required.
- Change the association table to no longer be constructed as a table and
  instead to be constructed as another model.
- Fix bug where some properties were incorrectly picked from a reference even
  though they existed locally (only impacts relationship properties where, for
  example, `x-secondary` was defined both on the relationship property in
  `allOf` and on the referenced model).
- Add check enforcing unique `x-tablename` values.
- Add check enforcing unique `x-secondary` values.

## Version 1.5.4 - 2020-10-10

- Refactor the models file generation to use the artifacts from the schemas.
- Add `build_json` and `build_yaml` interfaces which can be used to produce a
  package with the models.
- Changed output of build_json and build_yaml to be contained within a project
  directory.
- Add support for building sdist or wheel distributable archive.
- Drop support for Python 3.6 and add support for Python 3.9.

## Version 1.5.4 - 2020-08-30

- Move `description` to be a top level property artifact for every property.

## Version 1.5.3 - 2020-08-29

- Correct `format` key to no longer have a trailing `_` for artifacts.

## Version 1.5.2 - 2020-08-29

- Expose function that collects artifacts for the models.
- Expose function that collects artifacts for the model properties.

## Version 1.5.1 - 2020-08-23

- Add support for arbitrary mix in classes.

## Version 1.5.0 - 2020-08-22

- Add support for generic `format` for `string` that are treated like a
  `string` without a `format`.
- Change constructable check to no longer check the schema of `x-tablename`
  and `x-inherits`.
- Change schema validation to process properties even if the model is not
  valid.
- Add interface to check un-managed models for the reason why they are not
  managed.

## Version 1.4.3 - 2020-08-16

- Remove dependency on black

## Version 1.4.2 - 2020-08-16

- Fix bug where iterating over constructable schemas did not handle some
  exceptions
- Add black dependency back in

## Version 1.4.1 - 2020-08-09

- Remove black dependency

## Version 1.4.0 - 2020-08-09

- Add schemas pre-processor that extracts the required back references.
- Add foreign key pre-processor that extracts the required foreign keys.
- Add schema validation pre-processor.
- Add function that checks a specification.

## Version 1.3.0 - 2020-07-12

- Add support for generic JSON data for properties.
- Add support for `writeOnly`.
- Fix bug where the name of the foreign key column was based on the table name
  and not the property name.

## Version 1.2.0 - 2020-06-08

- Remove several bugs from the generated models file and integrate with
  `sqlalchemy-stubs`.
- Ring fence `black` dependency.
- add support for `__str__` and `__repr__` for model instances.

## Version 1.1.1 - 2020-05-17

- Add support for `readOnly`.
- Fix bug where TypedDIct types for `binary`, `date` and `date-time` string
  formats mapped to the incorrect python types.
- Fix bug where `to_dict` and `to_str` returned `null` for values that are not
  required and not nullable.

## Version 1.1.0 - 2020-04-05

- Add section of documentation for each example.
- Add support for keyword arguments for relationships used to define
  relationship arguments not specifically handled by an extension property.
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
- Add `from_str` and `to_str` to complement `from_dict` and `to_dict` for
  de-serializing and serializing from JSON.
- Ring fence jsonschema dependency into a facade.
- Add description from OpenAPI specification into the models file.

## Version 0.12.1 - 2020-01-12

- Fix bug where auto generating models file meant that multiple classes with
  the same name were registered with the base.

## Version 0.12.0 - 2020-01-04

- Fix bug where format and maxLength was not considered for the foreign key
  constructed for an object reference.
- Refactor object reference handling to be easier to understand.
- Add checking whether the column is automatically generated to determining
  the type of a column.
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
- Refactor handling array references to reduce scope of individual tests and
  make them easier to understand
- Add optional parameter that can be used to generate a models file for IDE
  auto complete and type hinting
- Add `from_dict` and `to_dict` to the type models file
- Add SQLAlchemy information to models file
- Add back references to models file

## Version 0.10.4 - 2019-12-18

- Fix bug where some static files where not included in the distribution.

## Version 0.10.1 - 2019-12-15

- Refactor column handler to first check the schema, then gather the required
  artifacts for column construction and then construct the column.
- Add support for DateTime.

## Version 0.10.0 - 2019-11-23

_Beta release_

- Add check for whether foreign key for relationship is already constructed
  before automatically constructing it.
- Add support for returning parent properties in the child `to_dict` call
  using `readOnly` properties.
- Add support for many to many relationships.

## Version 0.9.1 - 2019-11-11

- Fix bug where some static files where not included in the distribution.

## Version 0.9.0 - 2019-11-10

- Add `from_dict` and `to_dict` functions to all models that are used to
  construct a model from a dictionary and to convert a model instance to a
  dictionary, respectively.
- Add `x-foreign-key-column` extension property to define a custom foreign key
  constraint for many to one relationships.
- Add `x-composite-unique` extension property at the object level to construct
  unique constraints with multiple columns.
- Add `x-composite-index` extension property at the object level to construct
  indexes with multiple columns.
- Add support for one to one relationships.
- Fix bug where `allOf` merging would only return the properties of the last
  object instead of merging the properties.
- Add support for one to many relationships.

## Version 0.8.0 - 2019-11-03

- Add less verbose initialisation with `init_yaml` and `init_json`.
- Remove need for separate models file by exposing `Base` and constructed
  models at `open_alchemy.models`.
- Update name from OpenAPI-SQLAlchemy to OpenAlchemy

## Version 0.7.0 - 2019-10-27

- Add support for Python 3.6.
- Add connexion example application.
- Fixed bug where referencing a schema which uses allOf in many to one
  relationships does not merge the allOf statement.
- Fixed bug where a type hint that is not always exported from SQLAlchemy may
  cause an no member error.
- Add schema checking for extension properties.

## Version 0.6.3 - 2019-10-19

- Add support for backref for many to one relationships.
- Refactor to remove reference resolving decorator.
- Add integration tests for major features.

## Version 0.6.2 - 2019-10-19

- Add support for python 3.8.

## Version 0.6.1 - 2019-10-19

- Update name from openapi-SQLAlchemy to OpenAPI-SQLAlchemy. All urls are
  expected to keep working.

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
