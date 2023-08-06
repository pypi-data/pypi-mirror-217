"""Simple utilities.

"""


from functools import wraps
import numpy as np


def add_to_class(cls: type):
    """A decorator that add the decorated function
    to a class as its attribute.

    In development, this decorator could be used to
    dynamically overwrite attributes in a class for
    convenience.

    The implementation came from [Michael Garod](https://mgarod.medium.com/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6).

    :param type cls: The class to be added to.

    :Examples:
    ```py
    class A:
        def __init__(self) -> None:
            pass

    @add_to_class(A)
    def print_hi(self: A) -> None:
        print("Hi")

    >>> a = A()
    >>> a.print_hi()
    Hi
    ```
    """

    def decorator(method):
        """This decorator perform the attachment,
        then just return the original function.
        """

        @wraps(method)
        def add_this(*args, **kwargs):
            return method(*args, **kwargs)

        setattr(cls, method.__name__, add_this)
        return method

    return decorator


def unwrap_mapped_position(mapped_position: dict[str, np.ndarray]):
    return {k: v[0] for k, v in mapped_position.items()}
