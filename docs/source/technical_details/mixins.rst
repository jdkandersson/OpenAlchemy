.. _mixins:

Mixin Classes
=============

SQLAlchemy supports adding common functionality from a class to many other
classes through mixin classes. OpenAlchemy supports this through the
:samp:`x-mixins` extension property.

.. seealso::

    `SQLAlchemy mixin documentation <https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html#mixing-in-columns>`_
      Documentation for SQLAlchemy mixin.

The following rules apply to the :samp:`x-mixins` extension property:

* it can either be a string or a list of strings each of which defines one of
  the mixin classes and
* each value must be the fully qualified dotted name of the class to use as the
  mixin. Everything before the last dot will be used to import the module and
  everything after will be used to retrieve the class from the module.

The following example adds the :samp:`sqlalchemy_mixins.TimestampsMixin` to the
:samp:`Employee` model:

.. code-block:: yaml
    :linenos:

    Employee:
      type: object
      x-mixins: sqlalchemy_mixins.TimestampsMixin
      ...

Alternatively, multiple mixins can be defined using a list:

.. code-block:: yaml
    :linenos:

    Employee:
      type: object
      x-mixins:
        - sqlalchemy_mixins.TimestampsMixin
        - sqlalchemy_mixins.EagerLoadMixin
      ...

.. seealso::

    `sqlalchemy_mixins package <https://github.com/absent1706/sqlalchemy-mixins>`_
      Package that defines some helpful SQLAlchemy mixins.
