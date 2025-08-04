# pyproject.toml

The `pyproject.toml` file is a configuration file for Python projects. It was introduced in [PEP 518](https://peps.python.org/pep-0518/) and is the new standard for configuring Python projects. It is a TOML file and can be used to configure various aspects of a Python project, including the build system, project metadata, and tool-specific configurations.

## `[build-system]`

This table is used to specify the build system for the project. It is required if you want to build your project into a package (e.g., a wheel or sdist).

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

## `[project]`

This table is used to specify the metadata for the project. This is where you define the project's name, version, description, dependencies, and other information.

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A short description of my project."
requires-python = ">=3.8"
dependencies = [
    "requests",
    "click",
]
```

### Optional dependencies

You can also specify optional dependencies, which are dependencies that are not required for the project to function but are required for certain features.

```toml
[project.optional-dependencies]
dev = [
    "pytest",
    "ruff",
]
```

## Tool-specific configurations

You can also use `pyproject.toml` to configure various tools, such as `ruff`, `pytest`, and `uv`.

### `[tool.ruff]`

Ruff is a popular Python linter and formatter. You can configure it in `pyproject.toml` like this:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I"]
```

### `[tool.pytest.ini_options]`

Pytest is a popular Python testing framework. You can configure it in `pyproject.toml` like this:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
    "tests",
]
```

### `[tool.uv]`

uv is an extremely fast Python package installer, resolver, and manager, written in Rust. You can configure it in `pyproject.toml` like this:

```toml
[tool.uv]
dev-dependencies = [
    "pytest",
    "ruff",
]
```
