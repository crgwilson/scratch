# functools

The `functools` module provides a bunch of handy decorators for your functions

## Decorators

### @wraps

`functools.wraps` is a decorator which can be used to write your own decorators.

For a decorator with no parameters...

```python
from functools import wraps
from typing import Any, Callable

def decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> None:
        func_name = func.__name__

        print(f"I am going to call {func_name}")
        func(*args, **kwargs)
        print(f"I'm done calling {func_name}")

    return wrapper


@decorator
def example() -> None:
    print("I'm in here")


if __name__ == "__main__":
    example()

# I am going to call example
# I'm in here
# I'm done calling example
```

...and with parameters...

```python
from functools import wraps
from typing import Any, Callable

def decorator(example_value: str) -> Callable:
    def decorated(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            print(f"In the wrapper with example_value={example_value}")
            func(*args, **kwargs)

        return wrapper

    return decorated


@decorator(example_value="test")
def example() -> None:
    print("I'm in here")


if __name__ == "__main__":
    example()

# In the wrapper with example_value=test
# I'm in here
```

## Caching

### @lru_cache

Memorize (ie: cache) the result of calling the decorated function. Results are
stored in cache based on the args and kwargs passed into the underlying function.

You can control the size of your cache by using the `maxsize=<int>` parameter on
the `lru_cache` decorator. Also note that setting this to `None` will create a
cache with no size limit.

Once your cache hits its size limit it will evict the "least recently used" value.

```python
from functools import lru_cache

from some_lib import run_expensive_operation

@lru_cache(maxsize=32)
def this_is_expensive() -> int:
    result = run_expensive_operation()
    return result


if __name__ == "__main__":
    output: int = this_is_expensive()

    print(f"Got value {output}")
```

A function wrapped with `functools.lru_cache` will have a few extra functions attached
to it.

`wrapped_func.cache_parameters()` will give you a `dict` of the parameters which
were given to `lru_cache`

`wrapped_func.cache_info()` returns a `NamedTuple` containing some stats regarding
the effectiveness of your cache (`hits`, `misses`, `maxsize`, `currsize`)

`wrapped_func.cache_clear()` clears out any existing cache when called

`wrapped_func.__wrapped__` is the original underlying function

### @cache

The `functools.cache` decorator is just a shorthand way of calling `lru_cache(maxsize=None)`

For more info on `lru_cache` check out the above section

### @cached_property

The `functools.cached_propery` decorator is a shorthand way of applying both the
`@cache` and `@property` decorators onto a method

## functools: Further reading

[functools docs][docs]

[docs]:https://docs.python.org/3/library/functools.html "https://docs.python.org/3/library/functools.html"
