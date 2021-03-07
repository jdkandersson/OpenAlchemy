Type Mapping
============

OpenAlchemy translates OpenAPI types to SQLalchemy types using the
following mappings:

+----------------------+------------------------+-------------------------+---------------------------+
| OpenAPI type         | OpenAPI format         | SQLAlchemy type         | Python type               |
+======================+========================+=========================+===========================+
| :samp:`integer`      | :samp:`undefined`      | :samp:`Integer`         | :samp:`int`               |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`int32`          | :samp:`Integer`         | :samp:`int`               |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`int64`          | :samp:`BigInteger`      | :samp:`int`               |
+----------------------+------------------------+-------------------------+---------------------------+
| :samp:`number`       | :samp:`undefined`      | :samp:`Float`           | :samp:`float`             |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`float`          | :samp:`Float`           | :samp:`float`             |
+----------------------+------------------------+-------------------------+---------------------------+
| :samp:`string`       | :samp:`undefined`      | :samp:`String`          | :samp:`str`               |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`password`       | :samp:`String`          | :samp:`str`               |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`byte`           | :samp:`String`          | :samp:`str`               |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`binary`         | :samp:`LargeBinary`     | :samp:`bytes`             |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`date`           | :samp:`Date`            | :samp:`datetime.date`     |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`date-time`      | :samp:`DateTime`        | :samp:`datetime.datetime` |
+----------------------+------------------------+-------------------------+---------------------------+
|                      | :samp:`<other>`        | :samp:`String`          | :samp:`str`               |
+----------------------+------------------------+-------------------------+---------------------------+
| :samp:`boolean`      |                        | :samp:`Boolean`         | :samp:`bool`              |
+----------------------+------------------------+-------------------------+---------------------------+

:samp:`type` as an array is supported, however, exactly one type (other than
:samp:`null`) is required.

String
------

OpenAPI optionally allows the :samp:`maxLength` property for :samp:`strings`. This is
translated to the :samp:`length` argument for the SQLAlchemy :samp:`String`, which is set
to :samp:`None` if :samp:`maxLength` is :samp:`undefined`.

Password
--------

The same :samp:`maxLength` information as for :samp:`String` also applies.

.. note:: The :samp:`password` format under the hood is the same as :samp:`String`. No
    special protection (such as encryption) is added.

Byte
------

This format is for base64 encoded binary data. The same :samp:`maxLength`
information as for :samp:`String` also applies.

Binary
------

The same :samp:`maxLength` information as for :samp:`String` also applies. The codec is
assumed to be utf-8.

DateTime
--------

OpenAPI supports the inbuilt :samp:`date-time` format for a :samp:`string`. This is mapped
to the :samp:`DateTime` SQLAlchemy type. Currently, time zones are not supported.
Database best practice is to store everything in UTC. Applications, such as web
front ends, should convert to UTC as early as possible and localize a date and
time as late as possible.

.. _x-json:

JSON
----

SQLAlchemy supports generic data through the :samp:`JSON` type. OpenAlchemy
supports this through adding the :samp:`x-json` extension property to any
property of a model. This means that OpenAlchemy will ignore the true type of
the property and instead create a JSON column. For example, the :samp:`data`
property of the following :samp:`Employee` object is a generic JSON data store:

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
        data:
          type: object
          x-json: True

.. note:: If you are using the SQLAlchemy ORM do not use a JSON property as the
    primary key. This is technically valid although the unique identification
    logic in SQLAlchemy does not support this.

.. seealso::

    `SQLAlchemy JSON <https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.JSON>`_
      Documentation for the SQLAlchemy JSON type.
