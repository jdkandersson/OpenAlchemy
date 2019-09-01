References
==========

Using *$ref* statements, *openapi* allows you to reference other parts of the
schemas section. This means that a single definition for a *property* of an
*object* can be used for multiple *objects*. This pattern is supported by
*openapi-SQLAlchemy*. For example, the following *openapi* specification makes
use of references:

.. literalinclude:: ../../../examples/ref-example-spec.yml
