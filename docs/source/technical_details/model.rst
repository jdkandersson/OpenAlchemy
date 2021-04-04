.. _model-kwargs:

Miscellaneous Model Arguments
=============================

SQLAlchemy allows for special parameters, such as :samp:`__mapper_args__` that
change the behavior of a model. OpenAlchemy supports this by adding the
:samp:`x-kwargs` extension property for a schema. For example, the following
schema defines :samp:`__mapper_args__` for the *Employee* schema:

.. literalinclude:: ./model/kwargs.yaml
    :language: yaml
    :linenos:

Note that the following restrictions apply:

* the value must be an object,
* the keys of the object must be strings,
* the keys must start and end with :samp:`__` and
* keys cannot be:

    * :samp:`__tablename__` and
    * :samp:`__table_args__`.

Also note that no verification, beyond the above, is done before adding the
kwargs to the SQLAlchemy model.

.. _schema-name:

Define Custom Schema name
-------------------------

With some databases you can group tables into schemas. OpenAlchemy supports
this with the model extension property :samp:`x-schema-name` that is optionally
defined alongside :samp:`__tablename__`. It takes the name of the schema, for
example, the string :samp:`company`.

.. seealso::

    `SQLAlchemy specifying the schema name <https://docs.sqlalchemy.org/en/14/core/metadata.html#specifying-the-schema-name>`_
      Documentation for defining the schema name.
