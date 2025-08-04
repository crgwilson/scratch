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

### `[tool.mypy]`

MyPy is a static type checker for Python. To enable the strictest possible type checking, you can use the `strict = true` option, which enables a comprehensive set of strictness flags. You can also enable individual strictness flags for more granular control.

```toml
[tool.mypy]
# Enable all strictness flags
strict = true

# Alternatively, enable individual strictness flags:
# disallow_untyped_defs = true
# disallow_incomplete_defs = true
# check_untyped_defs = true
# disallow_untyped_calls = true
# disallow_untyped_decorators = true
# warn_unused_ignores = true
# warn_redundant_casts = true
# warn_return_any = true
# no_implicit_optional = true
# strict_optional = true
# ignore_missing_imports = false
# disallow_any_unimported = true
# disallow_any_untyped = true
# disallow_any_decorated = true
# disallow_any_explicit = true
# disallow_any_expr = true
```

### `[tool.ruff]` (Strict Linting)

To make Ruff linting as strict as possible, you can select a very broad range of linting rules. Ruff supports many rule categories, and you can enable them all or pick and choose.

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
# Select all available rule categories for maximum strictness.
# Be aware that this might introduce a large number of warnings/errors
# that you'll need to address.
select = [
    "ALL",
]
# You can also explicitly ignore specific rules if they are too strict for your project
# ignore = ["E501", "F401"]

# Enable specific strict checks
# For example, to disallow 'print' statements or 'pdb' imports:
# [tool.ruff.lint.per-file-ignores]
# "**/__init__.py" = ["F401"] # Ignore unused imports in __init__.py

# [tool.ruff.lint.isort]
# known-first-party = ["my_project"]

# [tool.ruff.lint.flake8-annotations]
# allow-untyped-decorators = false
# allow-untyped-base-classes = false

# [tool.ruff.lint.flake8-bugbear]
# extend-immutable-calls = ["fastapi.Depends", "fastapi.Query"]
```

**Note on `uv` and Linting:** `uv` is primarily a package installer, resolver, and manager. It does not have built-in linting capabilities or support for linting plugins. For linting, you should rely on dedicated tools like `ruff` or `flake8` (configured as shown above).
