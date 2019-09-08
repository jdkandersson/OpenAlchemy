"""Used to separate tests of decorators and underlying functions."""

import json
import os
import typing


def testing_guard(*, environment_name: str):
    """
    Apply decorator only in production.

    Decorator that only applies another decorator if the appropriate
    environment variable is not set.

    Args:
        environment_name: The name of the environment variable to check.

    Returns:
        Decorator function.

    """

    def decorator(decorator_func: typing.Callable) -> typing.Callable:
        def replacement(original_func: typing.Callable) -> typing.Callable:
            # Creating decorated function
            decorated_func = decorator_func(original_func)

            def apply_guard(*args, **kwargs):
                """Pick between decorated and original based on environment."""
                if os.getenv(environment_name) is not None:
                    # Noting application of decorator
                    decorator_trace_key = "DECORATOR_TRACE"
                    if os.getenv(decorator_trace_key) is not None:
                        # Building trace for call
                        trace = {
                            "function_name": str(decorator_func),
                            "closures": [
                                str(closure.cell_contents)
                                for closure in decorator_func.__closure__
                                if closure.cell_contents
                            ]
                            if decorator_func.__closure__
                            else None,
                        }
                        # Recording trace
                        current_trace = json.loads(os.getenv(decorator_trace_key))
                        current_trace.append(trace)
                        os.environ[decorator_trace_key] = json.dumps(current_trace)

                    # Use original function
                    return original_func(*args, **kwargs)
                # Use decorated function
                return decorated_func(*args, **kwargs)

            return apply_guard

        return replacement

    return decorator
