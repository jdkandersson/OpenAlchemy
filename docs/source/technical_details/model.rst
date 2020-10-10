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
