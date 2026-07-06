# pytest

Pytest is my preferred unit testing framework for python projects

## pytest: Usage

Example project layout:

```console
project
├── LICENSE
├── README.md
├── project
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
├── setup.py
├── tests
│   ├── conftest.py
│   ├── test_main.py
│   └── test_utils.py
└── tox.ini
```

### pytest: Unit tests

As shown above unit tests should be...

* Confined to a `tests` directory (ideally outside of your module)
* Be saved in a `test_<name>.py` file
* Be defined as a function named `test_<something>`

```python
# project/tests/test_utils.py
from project.utils import return_an_int

def test_return_an_int() -> None:
    result = return_an_int()
    assert isinstance(result, int)
```

#### Unit tests: Exceptions

You can test that a chunk of code throws an exception using the `pytest.raises` context...

```python
# project/tests/test_utils.py
import pytest

from project.utils import throw_an_exception

def test_something() -> None:
    with pytest.raises(Exception) as err:
        throw_an_exception()

    assert err
```

#### Unit tests: parametrize

You can run many unit tests with minor "parametrized" variations using `@pytest.mark.parametrize`
decorator.

It expects two parameters...

1. A string containing a comma delimited list of parameter names
1. A list of tuples containing all the parameter values

```python
import pytest

@pytest.mark.parametrize(
    "number,expected",
    [
      (1, 1),
      (2, 4),
      (3, 9),
    ],
)
def test_square(number, expected) -> None:
    assert number^2 == expected
```

The above example will run three tests with each of the provided tuples

### pytest: Fixtures

Custom fixtures needed for your unit tests should...

* Live in `project/tests/conftest.py`
* Be decorated with `@pytest.fixture`
* `yield` rather than `return`

Pytest fixtures are accessible within unit tests so long as your test accepts an
argument matching the name of an existing fixture.

```python
# project/tests/conftest.py
import pytest

@pytest.fixture
def some_mock_object():
    mock_object = create_some_mock_object()  # pretend this would work
    yield mock_object
    # cleanup your object here if you need to

# project/tests/test_utils.py
def test_something(some_mock_object) ->:
    assert some_mock_object.works()
```

#### Fixtures: scope

Fixtures can be given a scope to determine when they are destroyed after being
requested by a test.

* `function` is the default scope and will result in the fixture being destroyed
  at the end of the test
* `class` scope will destroy fixtures after the last test in the class
* `module` scope will destroy fixtures after the last test in the module
* `package` scope will destroy fixtures after the last test in the package
* `session` scope will destroy fixtures at the very end of the pytest session

The fixture scopes I use the most often are `session` and `function`

```python
# project/tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def long_lived_fixture:
    ...

@pytest.fixture
def short_lived_fixture()
    ...
```

#### Fixtures: monkeypatch

The `monkeypatch` fixture lets you replace objects in your source code with mock
objects to help make things more easily testable.

```python
# project/project/main.py
from pathlib import Path

def getssh():
    return f"{Path.home()}/.ssh"

# project/tests/test_main.py
from pathlib import Path

from project.main import getssh

def test_getssh(monkeypatch):
    def mockreturn():
        return Path("/abc")

    # Replace the "home" attribute (in this case its a function) with
    # a mock function of our own
    monkeypatch.setattr(Path, "home", mockreturn)
    assert getssh() == Path("/abc")
```

You can also monkeypatch something globally. This example will prevent `requests`
from making any real outgoing http requests during any test in the project.

```python
# project/tests/conftest.py
import pytest

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")
```

## pytest: Further reading

* [github][github]
* [docs][docs]

[github]:http://github.com/pytest-dev/pytest "http://github.com/pytest-dev/pytest"
[docs]:https://docs.pytest.org/en/stable/contents.html "https://docs.pytest.org/en/stable/contents.html"
