.. contents::

Welcome to OpenAPI-SQLAlchemy's documentation!
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
from *openapi_sqlalchemy.models*::

    from openapi_sqlalchemy import Base
    from openapi_sqlalchemy import Employee


.. _how-does-it-work:

How Does It Work?
-----------------

Given a name for a schema, *OpenAPI-SQLAlchemy* looks for that schema in the
schemas section of the specification. The schema must have the *x-tablename*
property which defines the name of the table. The schema is required to be an
*object*. For each *property* of the schema, a column is generated for the
table mapping OpenAPI types to equivalent SQLAlchemy types.

On top of the information in the OpenAPI specification, certain extension
properties are used to define the database schema. The following specification
defines the format and provides a description for each of the supported
extension properties.

.. literalinclude:: ../../openapi_sqlalchemy/helpers/get_ext_prop/extension-schemas.json

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
to the *models* module that is available from OpenAPI-SQLAlchemy.
