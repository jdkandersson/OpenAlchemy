.. role:: python(code)
   :language: python

.. contents::

Welcome to OpenAlchemy's documentation!
==============================================

Translates OpenAPI schemas to SQLAlchemy models to reduce duplication when
defining your API and database models. Any required additions to the OpenAPI
specification are compliant with the OpenAPI standard.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   examples/index
   technical_details/index


.. _getting-started:

Getting Started
---------------

If you have the following OpenAPI specification:

.. literalinclude:: ../../examples/simple-example-spec.yml

To use SQLAlchemy to retrieve *Employees* from a database you need the
following *models.py* file:

.. literalinclude:: ../../examples/simple_models.py

The *Base* for the SQLAlchemy models and the *Employee* model is now available
from *open_alchemy.models*::

    from open_alchemy.models import Base
    from open_alchemy.models import Employee

Interfaces
----------

The most user friendly interfaces are the :ref:`init-yaml` and
:ref:`init-json` interfaces. The :ref:`init-model-factory` interface is a
lower level interface which has fewer dependencies but is not as user
friendly.


.. _init-yaml:

*init_yaml*
^^^^^^^^^^^

The *init_yaml* interface requires the *PyYAML* library to be installed. The
*init_yaml* interface accepts the following arguments:

* *spec_filename*: The name of the file as a positional argument. The file
  must by a YAML file.
* *base*: The SQLAlchemy declarative base as an optional keyword only
  argument. It is used to as the base class for all SQLAlchemy models. If it
  is not passed in, a new declarative base is constructed.
* *define_all*: Whether to pre-define the SQLAlchemy models as an optional
  keyword only argument. If it is *True*, all schemas with the *x-tablename*
  property are constructed as a part of the initialization. Defaults to
  *True*.

The return value is a tuple consisting of:

* *Base*: The SQLAlchemy declarative based used for the models. It is also
  importable: :python:`from open_alchemy.models import Base`.
* *model_factory*: The factory that can be used to construct the SQLAlchemy
  models using the name of the schema in the OpenAPI specification. All
  constructed models are added to the *open_alchemy.models* module and are
  importable. For example: :python:`from open_alchemy.models import Employee`.


.. _init-json:

*init_json*
^^^^^^^^^^^

The *init_json* interface is similar to the :ref:`init-yaml` interface except
that *spec_filename* must be a JSON file and *PyYAML* is not a required
dependency.


.. _init-model-factory:

*init_model_factory*
^^^^^^^^^^^^^^^^^^^^

The *init_model_factory* interface is less user friendly but perhaps of
interest to advanced users. It accepts the specification in dictionary format
(so it has fewer dependencies than :ref:`init-yaml` and :ref:`init-json`) and
does not construct a declarative base. It accepts the following parameters:

* *base*: The SQLAlchemy declarative base as a keyword only argument. It is
  used to as the base class for all SQLAlchemy models.
* *spec*: The OpenAPI specification as a dictionary as a keyword only
  argument.
* *define_all*: Whether to pre-define the SQLAlchemy models as an optional
  keyword only argument. If it is *True*, all schemas with the *x-tablename*
  property are constructed as a part of the initialization. Defaults to
  *False*.

The return value is the *model_factory* as defined as part of the return value
of :ref:`init-yaml`.


.. _how-does-it-work:

How Does It Work?
-----------------

Given a name for a schema, *OpenAlchemy* looks for that schema in the
schemas section of the specification. The schema must have the *x-tablename*
property which defines the name of the table. The schema is required to be an
*object*. For each *property* of the schema, a column is generated for the
table mapping OpenAPI types to equivalent SQLAlchemy types.

On top of the information in the OpenAPI specification, certain extension
properties are used to define the database schema. The following specification
defines the format and provides a description for each of the supported
extension properties.

.. literalinclude:: ../../open_alchemy/helpers/get_ext_prop/extension-schemas.json

To find out more about an extension property, go to the following section of
the documentation:

+-----------------+-------------------------+
| property        | documentation section   |
+=================+=========================+
| x-backref       | :ref:`backref`          |
+-----------------+-------------------------+
| x-primary-key   | :ref:`primary-key`      |
+-----------------+-------------------------+
| x-autoincrement | :ref:`autoincrement`    |
+-----------------+-------------------------+
| x-index         | :ref:`index`            |
+-----------------+-------------------------+
| x-unique        | :ref:`unique`           |
+-----------------+-------------------------+
| x-foreign-key   | :ref:`foreign-key`      |
+-----------------+-------------------------+
| x-tablename     | :ref:`how-does-it-work` |
+-----------------+-------------------------+

The SQLAlchemy *Base* and any constructed database models are dynamically added
to the *models* module that is available from OpenAlchemy.
