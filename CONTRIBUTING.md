# Contributing

The project welcomes contributions in any form! They could take the form of
reporting bugs, feature requests, updates to documentation and even
enhancements to the code.

To help smooth out the contributions, here are some guidelines of conventions
used in the code (the list will evolve over time):

## General

- If you find anything not in line with these guidelines, it is because this
  repository takes the approach of "if youchange it please align it to the
  current standards". Please correct the code to follow these guidelines.

## Code

- The maximum line length is 89 in Python files.
- Import modules as namespaces. For example, instead of `from enum import auto`
  use `import enum` and then `enum.auto`.
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

- Use type hints, avoid using `typing.Any` where reasonable.
- 100% code coverage is required (except as configured with a documented
  reason).
- In error messages, explain what has gone wrong and how to fix it.
- If an argument is optional in a function, any functions that it calls should
  no longer make the argument optional.
- Take note of the tools used in the pipeline for code quality checks. Any
  disabling of any check must be documented with a reason.
- Note changes in the changelog.
- Any raised exceptions should inherit from
  `open_alchemy.exceptions.BaseError`. Exception handling should specify which
  exception is being handled (e.i. more specific than `Exception`.
- Update the readme with any significant new features
- Update the documentation and examples, if appropriate
- Functions that are intended for re-use across the code base (e.g. helper
  functions) should use keyword only arguments for increased clarity. Private
  module/ class functions may optionally use positional arguments for enhanced
  execution speed.
  
## Tests

- In tests, preferable use parameterization instead of a for loop in the test
  body.
- Test docstrings should use the following structure:

  ```Python
  """
  GIVEN <preconditions>
  WHEN <an action is taken>
  THEN <this outcome is expected>
  """
  ```

- Separate the code for GIVEN, WHEN and THEN in tests using a single blank line
  to indicate where each piece starts
- For parameterization, use `pytest.param` and provide a value for the `id`
  argument
- If the number of parameters for a test becomes large, take the list out of the
  decorator and make it a module variable.

## Documentation

- Use passive language in documentation.
- The maximum line length is 80 in the documentation.

