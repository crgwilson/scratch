# Typing

Notes regarding python type hints and how to validate them

## Type hints

Type hints were added in python 3.5, and while they are not enforced during
runtime they can be another way to test / lint your code pre-commit.

We can annotate variables, function parameters, and returns with their expected
type.

For a really simple example, it would change this...

```python
def repeat(word, repeats=1):
    return_str = ""

    for i in range(0, repeats):
      return_str = return_str + word

    return return_str
```

...to this...

```python
def repeat(word: str, repeats: int = 1) -> str:
    return_str: str = ""

    for i in range(0, repeats):
        return_str = return_str + word

    return return_str
```

These type annotations can be used with built-in types, custom classes,
and other objects from the `typing` lib

These `typing` objects can be found in the below documentation, but the gist is
there is support for

- Dicts
- Lists
- Tuples
- Maps
- Callables (like functions, etc)
- Literal values
- Generics

### Type hints: Aliases

If you have a function which is expecting a more complicated type (like a dict)
you can define that separately so you can reference it easily in multiple places.

```python
from typing import Dict, List

list_of_dicts = List[Dict[str, int]]

def some_function(some_value: list_of_dicts):
    pass
```

### Type hints: Custom types

You can also define your own custom types using the `NewType()` function from
`typing`.

```python
from typing import List, NewType

ShoppingList = NewType("ShoppingList", List[str])
```

### Type hints: None vs NoReturn

When you have a function which doesn't return a value you should annotate
the return with `None`, like so...

```python
def my_func() -> None:
    pass
```

But `typing` also has `NoReturn`, so if you use `None` when you're not returning
anything when do you use that?

Well, `NoReturn` is for when a chunk of code never returns at all. For example, if
it just raises an exception.

```python
from typing import NoReturn

def dont_return() -> NoReturn:
    raise Exception("rip")
```

### Type hints: Further reading

[PEP 484](https://www.python.org/dev/peps/pep-0484/)
[typing docs](https://docs.python.org/3/library/typing.html)

### Validating Type hints with MyPy

[MyPy](http://mypy-lang.org/) is a tool which checks type annotations.

I can be configured along with all of your other linting tools in `setup.cfg`.
For more info on the specific settings available
[check out the docs](https://mypy.readthedocs.io/en/stable/config_file.html)

### MyPy: reveal_type

mypy provides a `reveal_type()` function to help out which writing
type annotations. Whenever you come across a variable and aren't quite sure
_what_ it is, you can pop `reveal_type(my_var)` in. It will raise an exception
containing the appropriate type, and remove itself from your code.

#### MyPy: Further reading

[mypy docs](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
