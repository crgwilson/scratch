# Tox

Tox is a generic virtualenv management and test tool for Python projects.

## Tox: Basic Usage

To run tests with tox, you typically navigate to your project's root directory (where `tox.ini` is located) and simply run:

```bash
tox
```

This will create virtual environments, install dependencies, and run the commands defined in `tox.ini` for each specified environment.

## Tox: Configuration (`tox.ini`)

Tox is configured via a `tox.ini` file in the root of your project. This file defines different test environments, their dependencies, and the commands to run.

Example `tox.ini`:

```ini
[tox]
env_list = py39,py310

[testenv]
deps =
    pytest
commands =
    pytest
```

### `[tox]` section

*   `env_list`: Defines a comma-separated list of environments to run by default.

### `[testenv]` section

This section defines the default settings for all test environments. You can override these settings for specific environments (e.g., `[testenv:py39]`)

*   `deps`: List of dependencies to install in the virtual environment before running tests.
*   `commands`: List of shell commands to execute within the virtual environment.

## Tox: Running Specific Environments

You can run specific tox environments using the `-e` flag:

```bash
tox -e py39
```

To run multiple specific environments:

```bash
tox -e py39,py310
```

## Tox: Recreating Environments

If you need to force tox to recreate a virtual environment (e.g., due to dependency issues or changes in `deps`):

```bash
tox -r
```

Or for a specific environment:

```bash
tox -r -e py39
```

## Tox and uv

To integrate `uv` with `tox`, the recommended approach is to use the `tox-uv` plugin. This plugin replaces `virtualenv` and `pip` with `uv` within your `tox` environments, offering significant performance improvements.

### Installation

First, install `tox-uv` in the same Python environment where `tox` is installed. If you're using `uv` to manage your tools, you can install both `tox` and `tox-uv` like this:

```bash
uv tool install tox --with tox-uv
```

### Configuration (`tox.ini`)

Once `tox-uv` is installed, you can configure your `tox.ini` to leverage `uv`. `tox-uv` provides new runner types for your test environments.

Here's an example of how to configure a `testenv` to use `uv` and a `uv.lock` file:

```ini
[testenv]
runner = uv-venv-lock-runner
extras = dev
commands = pytest
```

*   `runner = uv-venv-lock-runner`: This explicitly tells `tox` to use the `uv-venv-lock-runner`, which enables `uv.lock` file support for this environment.
*   `extras = dev`: If your project uses optional dependencies defined in `pyproject.toml` (e.g., `[project.optional-dependencies] dev = [...]`), this will instruct `uv` to install those `dev` extras from your `uv.lock` file.

For environments not using a `uv.lock` file, you can use `runner = uv-venv-runner`.

### Automatic Provisioning

You can also ensure `tox-uv` is automatically provisioned by `tox` by adding it to the `requires` section of your `tox.ini`:

```ini
[tox]
requires =
    tox>=4
    tox-uv>=1
env_list = py39,py310
```

## Tox: Further Reading

*   [Tox Documentation](https://tox.wiki/en/latest/)
*   [tox-uv GitHub Repository](https://github.com/tox-dev/tox-uv)
