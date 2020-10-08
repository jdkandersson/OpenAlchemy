# Contributing

The project welcomes contributions in any form! They could take the form of
reporting bugs, feature requests, updates to documentation and even
enhancements to the code.

To help smooth out the contributions, here are some guidelines of conventions
used in the code (the list will evolve over time):

- Import modules as namespaces. For example, instead of `from enum import auto`
  use `import enum` and then `enum.auto`.
- In tests, preferable use parameterization instead of a for loop in the test
  body.
- Use passive language in documentation.
- Use the following pattern for docstring:

  ```Python
  def func(arg1: int, arg2: str = "hi") -> float:
      """
      Single line explaining the function.

      More detailed information (such as exception that are raised, algorithms,
      ...) if required.

      Args:
          arg_1: Description 1.
          arg_2: Description 2.

      Returns:
          Information about the return value.

      """
  ```

  The `Args` are not needed if there are no arguments and `Returns` is not
  needed if `None` is returned.

- Use type hints
- 100% code coverage is required (except as configured with a documented
  reason).
- In error messages, explain what has gone wrong and how to fix it.
- If an argument is optional in a function, any functions that it calls should
  no longer make the argument optional.
- Take not of the tools used in the pipeline for code quality checks. Any
  disabling of any check must be documented with a reason.
