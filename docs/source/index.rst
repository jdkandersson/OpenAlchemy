.. role:: python(code)
   :language: python

.. contents::

Welcome to OpenAlchemy's documentation!
==============================================

Translates OpenAPI schemas to SQLAlchemy models to reduce duplication when
defining your API and database models. Any required additions to the OpenAPI
specification are compliant with the OpenAPI standard.

.. seealso::

   `Online Editor <https://editor.openalchemy.io/>`_
      Online editor including schema validation.

.. _getting-started:

Getting Started
---------------

If you have the following OpenAPI specification:

.. literalinclude:: ../../examples/simple/example-spec.yml
    :language: yaml
    :linenos:

To use SQLAlchemy to retrieve :samp:`Employees` from a database you need the
following :samp:`models.py` file:

.. literalinclude:: ../../examples/simple/models.py
    :language: python
    :linenos:

The :samp:`Base` for the SQLAlchemy models and the :samp:`Employee` model is
now available from :samp:`open_alchemy.models`::

    from open_alchemy.models import Base
    from open_alchemy.models import Employee

Interfaces
----------

The most user friendly interfaces are the :ref:`init-yaml` and
:ref:`init-json` interfaces. The :ref:`init-model-factory` interface is a
lower level interface which has fewer dependencies but is not as user
friendly.

.. _init-yaml:

:samp:`init_yaml`
^^^^^^^^^^^^^^^^^

Used to initialize the SQLAlchemy models based on a YAML OpenAPI specification
which has been extended with any relevant OpenAlchemy extension properties.

The :samp:`init_yaml` interface requires the :samp:`PyYAML` library to be
installed. The :samp:`init_yaml` interface accepts the following arguments:

* :samp:`spec_filename`: The name of the file as a positional argument. The
  file must by a YAML file.
* :samp:`base`: The SQLAlchemy declarative base as an optional keyword only
  argument. It is used to as the base class for all SQLAlchemy models. If it
  is not passed in, a new declarative base is constructed.
* :samp:`models_filename`: The name of the file where the SQLAlchemy models
  will be written as an optional keyword only argument.
* :samp:`spec_path`: The path to the OpenAPI specification (what would need to
  be passed to the :samp:`open` function to read the file) as an optional
  keyword only argument. Used to support remote references.

.. note:: the :samp:`define_all` parameter has been removed and OpenAlchemy
  behaves as though it is set to :samp:`True`.

The return value is a tuple consisting of:

* :samp:`Base`: The SQLAlchemy declarative based used for the models. It is
  also importable: :python:`from open_alchemy.models import Base`.
* :samp:`model_factory`: The factory that can be used to construct the
  SQLAlchemy models using the name of the schema in the OpenAPI specification.
  All constructed models are added to the :samp:`open_alchemy.models` module
  and are importable. For example:
  :python:`from open_alchemy.models import Employee`.

.. _init-json:

:samp:`init_json`
^^^^^^^^^^^^^^^^^

The :samp:`init_json` interface is similar to the :ref:`init-yaml` interface
except that :samp:`spec_filename` must be a JSON file and :samp:`PyYAML` is not
a required dependency.

.. _init-model-factory:

:samp:`init_model_factory`
^^^^^^^^^^^^^^^^^^^^^^^^^^

The :samp:`init_model_factory` interface is less user friendly but perhaps of
interest to advanced users. It accepts the specification in dictionary format
(so it has fewer dependencies than :ref:`init-yaml` and :ref:`init-json`) and
does not construct a declarative base. It accepts the following parameters:

* :samp:`base`: The SQLAlchemy declarative base as a keyword only argument. It
  is used to as the base class for all SQLAlchemy models.
* :samp:`spec`: The OpenAPI specification as a dictionary as a keyword only
  argument.
* :samp:`models_filename`: The name of the file where the SQLAlchemy models
  will be written as an optional keyword only argument.

.. note:: the :samp:`define_all` parameter has been removed and OpenAlchemy
  behaves as though it is set to :samp:`True`.

The return value is the :samp:`model_factory` as defined as part of the return
value of :ref:`init-yaml`.

.. _build-yaml:

:samp:`build_yaml`
^^^^^^^^^^^^^^^^^^

Used to build a package with the SQLAlchemy models (including type hints) based
on a YAML OpenAPI specification which has been extended with any relevant
OpenAlchemy extension properties.

The :samp:`build_yaml` interface requires the :samp:`PyYAML` library to be
installed. The :samp:`build_yaml` interface accepts the following arguments:

* :samp:`spec_filename`: The name of the OpenAPI specification file. The file
  must by a YAML file.
* :samp:`package_name`: The name of the package to be produced. This will be

  1. the name of the package if it is uploaded to a package index and
  2. the name that is used to import the models after they have been installed).

* :samp:`dist_path`: The directory to output the package files.
* :samp:`format_`: Optionally, the format of the package to build:

  * ``PackageFormat.NONE``: no package is built (default)
  * ``PackageFormat.SDIST``: a sdist package is built
  * ``PackageFormat.WHEEL``: a wheel package is built

  The formats can be combined with the bitwise operator "or" (``|``), for
  instance, building both sdist and wheel packages can be specified like this:

  .. code-block:: python

    format_=PackageFormat.SDIST|PackageFormat.WHEEL

  .. warning::

    In order to build a wheel distributable archive, the
    `wheel <https://pypi.org/project/wheel/>`_ package is necessary.

    It can be installed separately with ``pip install wheel``, or with
    OpenAlchemy directly with ``pip install OpenAlchemy[wheel]``.

.. _build-json:

:samp:`build_json`
^^^^^^^^^^^^^^^^^^

The :samp:`build_json` interface is similar to the :ref:`build-yaml` interface
except that :samp:`spec_filename` must be a JSON file and :samp:`PyYAML` is not
a required dependency.

.. _models-file:

Models File
-----------

:samp:`OpenAlchemy` can optionally generate a file with all the
:samp:`SQLAlchemy` models. Each model is constructed based on the
:samp:`OpenApi` schema. The class inherits from the :samp:`SQLAlchemy` model
defined on :samp:`open_alchemy.models`. The generated classes contain type
information only, they do not provide any additional functionality on top of
what the :samp:`SQLAlchemy` model provides. They are primarily
used to enable IDE auto-complete and type hint support. The models can be used
in the same way as the models that can be imported from
:samp:`open_alchemy.models` and provide the full functionality of
:samp:`SQLAlchemy` models. The following is a sample file generated for the
above example:

.. literalinclude:: ../../examples/simple/models_auto.py
    :language: python
    :linenos:

The following information is recorded in the models file:

* The name and type of each property of a schema.
* The :ref:`from-dict` and :ref:`to-dict` function signatures, including
  the type of the arguments and return values.
* The :ref:`from-str` and :ref:`to-str` function signatures, including
  the type of the arguments and return values.
* The properties created on instance objects due to any :ref:`backref`.
* Special SQLAlchemy properties for interacting with the database.
* The object and property descriptions from the OpenAPI specification in the
  class and function docstrings.

.. _backrefs:

.. note:: To be able to add relationships created by :samp:`x-backrefs` to the
    type annotations of the models file, the schema stored alongside a model,
    which is accessible at the :samp:`_schema` class variable (not a public
    interface so it should not be used or relied upon), will use the
    :samp:`x-backrefs` extension property to record the schema for all back
    references for the model. :samp:`x-backrefs` is not a public interface and
    should not be relied upon as it is subject to change.

It is worth noting that the auto-generated models cannot be imported directly.
The generated models are added to the :samp:`open_alchemy.models` package by the
:samp:`init_*` functions.

.. code-block:: python
  :linenos:

  from open_alchemy import init_yaml
  from open_alchemy import models

  init_yaml('openapi.yml')
  employee = models.Employee(name="David Andersson", division="Engineering")

To use the models in another project, refer to the `build_yaml`_ or `build_json`_
functions.

.. _model-utilities:

Model Utilities
---------------

There are a few common utility functions that are added to the models. The
:ref:`from-dict` utility function constructs a model instance from a
dictionary. The :ref:`to-dict` function converts a model instance to a
dictionary.

.. _from-dict:

:samp:`from_dict`
^^^^^^^^^^^^^^^^^

The :samp:`from_dict` function is available on all constructed models. It
accepts a dictionary and constructs a model instance based on the dictionary.
It is similar to :python:`Employee(**employee_dict)` with a few advantages:

* The dictionary based on which the model is constructed is checked against
  the schema used to define the model.
* If the model includes a relationship, the relationship is constructed
  recursively.

For example::

    >>> employee_dict = {
        "id": 1,
        "name": "David Andersson",
        "division": "engineering",
        "salary": 1000000,
    }
    >>> employee = Employee.from_dict(**employee_dict)
    >>> employee.name
    'David Andersson'

.. _de-ref:

.. note:: To be able to support relationships, the schema stored alongside a
    model, which is accessible at the :samp:`_schema` class variable (not a
    public interface so it should not be used or relied upon), won't store the
    actual schema for the referenced object. Instead, the :samp:`object` type
    is noted for the property alongside the :samp:`x-de-$ref` extension
    property which stores the name of the referenced model.

.. _from-str:

:samp:`from_str`
^^^^^^^^^^^^^^^^

The :samp:`from_str` function is available on all constructed models. It
accepts a JSON formatted string and constructs a model instance by
de-serializing the JSON string and then using :ref:`from-dict`. For example::

    >>> employee_str = '''{
        "id": 1,
        "name": "David Andersson",
        "division": "engineering",
        "salary": 1000000
    }'''
    >>> employee = Employee.from_str(employee_str)
    >>> employee.name
    'David Andersson'

.. _to-dict:

:samp:`to_dict`
^^^^^^^^^^^^^^^

The :samp:`to_dict` function is available on all constructed models. It
converts a model instance into a dictionary based on the schema that was used
to define the model. If the model includes a relationship, the :samp:`to_dict`
function is called recursively on the relationship.

For example::

    >>> employee_dict = {
        "id": 1,
        "name": "David Andersson",
        "division": "engineering",
        "salary": 1000000,
    }
    >>> employee = Employee.from_dict(**employee_dict)
    >>> employee.to_dict()
    {'id': 1, 'name': 'David Andersson', 'division': 'engineering', 'salary': 1000000}

.. seealso::
    :ref:`child-parent-reference`

.. _to-str:

:samp:`to_str`
^^^^^^^^^^^^^^

The :samp:`to_str` function is available on all constructed models. It converts
a model instance into a JSON formatted string by serializing the output of
:ref:`to-dict`.

For example::

    >>> employee_str = '''{
        "id": 1,
        "name": "David Andersson",
        "division": "engineering",
        "salary": 1000000
    }'''
    >>> employee = Employee.from_str(employee_str)
    >>> employee.to_str()
    '{"id": 1, "name": "David Andersson", "division": "engineering", "salary": 1000000}'

.. _str:

:samp:`__str__`
^^^^^^^^^^^^^^^

It is possible to convert any model instance to a string using the
:python:`str` function. This is supported as there is a :samp:`__str__` alias
for the :ref:`to-str` function.

.. _repr:

:samp:`__repr__`
^^^^^^^^^^^^^^^^

Each model includes a :samp:`__repr__` implementation to support calling
:python:`repr` in any model instance. The returned string is the source code
required to construct an equivalent model instance.

For example::

    >>> employee_dict = {
        "id": 1,
        "name": "David Andersson",
        "division": "engineering",
        "salary": 1000000,
    }
    >>> employee = Employee.from_dict(**employee_dict)
    >>> repr(employee)
    "open_alchemy.models.Employee(id=1, name='David Andersson', division='engineering', salary=1000000)"

.. _alembic:

Alembic
-------

The standard method for automatically generating database migrations for
alembic is supported. The following instructions show how to get started:

.. literalinclude:: ../../examples/alembic/readme.md
    :language: md

Extension Property Prefix
-------------------------

OpenAlchemy currently supports 2 extension property prefixes. The shorter
:samp:`x-` and the longer :samp:`x-open-alchemy-`. Both prefixes behave in the
same way. The longer prefix is offered to avoid extension property name clashes
with other tools.

.. _how-does-it-work:

How Does It Work?
-----------------

Given a name for a schema, :samp:`OpenAlchemy` looks for that schema in the
schemas section of the specification. The schema must have the
:samp:`x-tablename` property which defines the name of the table. The schema is
required to be an :samp:`object`. For each :samp:`property` of the schema, a
column is generated for the table mapping OpenAPI types to equivalent
SQLAlchemy types.

On top of the information in the OpenAPI specification, certain extension
properties are used to define the database schema. The following specification
defines the format and provides a description for each of the supported
extension properties.

.. literalinclude:: ../../open_alchemy/helpers/ext_prop/extension-schemas.json
    :language: json
    :linenos:

To find out more about an extension property, go to the following section of
the documentation:

+------------------------------+----------------------------------------------------+
| property                     | documentation section                              |
+==============================+====================================================+
| :samp:`x-backref`            | :ref:`backref`                                     |
+------------------------------+----------------------------------------------------+
| :samp:`x-uselist`            | :ref:`one-to-one`                                  |
+------------------------------+----------------------------------------------------+
| :samp:`x-secondary`          | :ref:`many-to-many`                                |
+------------------------------+----------------------------------------------------+
| :samp:`x-primary-key`        | :ref:`primary-key`                                 |
+------------------------------+----------------------------------------------------+
| :samp:`x-autoincrement`      | :ref:`autoincrement`                               |
+------------------------------+----------------------------------------------------+
| :samp:`x-index`              | :ref:`column-index`                                |
+------------------------------+----------------------------------------------------+
| :samp:`x-composite-index`    | :ref:`composite-index`                             |
+------------------------------+----------------------------------------------------+
| :samp:`x-unique`             | :ref:`column-unique`                               |
+------------------------------+----------------------------------------------------+
| :samp:`x-composite-unique`   | :ref:`composite-unique`                            |
+------------------------------+----------------------------------------------------+
| :samp:`x-foreign-key`        | :ref:`foreign-key`                                 |
+------------------------------+----------------------------------------------------+
| :samp:`x-tablename`          | :ref:`how-does-it-work`                            |
+------------------------------+----------------------------------------------------+
| :samp:`x-inherits`           | :ref:`x-inherits`                                  |
+------------------------------+----------------------------------------------------+
| :samp:`x-foreign-key-colum`  | :ref:`custom-foreign-key`                          |
+------------------------------+----------------------------------------------------+
| :samp:`x-mixins`             | :ref:`mixins`                                      |
+------------------------------+----------------------------------------------------+
| :samp:`x-backrefs`           | :ref:`Models File Note <backrefs>`                 |
+------------------------------+----------------------------------------------------+
| :samp:`x-de-$ref`            | :ref:`from_dict Note <de-ref>`                     |
+------------------------------+----------------------------------------------------+
| :samp:`x-dict-ignore`        | :ref:`One to Many Note <dict-ignore>`              |
+------------------------------+----------------------------------------------------+
| :samp:`x-generated`          | :ref:`Nullable Note <generated>`                   |
+------------------------------+----------------------------------------------------+
| :samp:`x-kwargs`             | * :ref:`Relationship kwargs <relationship-kwargs>` |
|                              | * :ref:`Model kwargs <model-kwargs>`               |
|                              | * :ref:`Column kwargs <column-kwargs>`             |
+------------------------------+----------------------------------------------------+
| :samp:`x-foreign-key-kwargs` | :ref:`Foreign Key kwargs <foreign-key-kwargs>`     |
+------------------------------+----------------------------------------------------+

The SQLAlchemy :samp:`Base` and any constructed database models are dynamically
added to the :samp:`models` module that is available from OpenAlchemy.

Technical Details
-----------------

.. toctree::
   :maxdepth: 3

   technical_details/index

Examples
--------

.. toctree::
   :maxdepth: 3

   examples/index

CLI
---

.. toctree::
   :maxdepth: 3

   cli
