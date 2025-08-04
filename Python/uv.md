# uv

uv is an extremely fast Python package installer, resolver, and manager, written in Rust. It is designed to be a drop-in replacement for `pip` and `pip-tools`.

## Installation

You can install `uv` with the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Common Commands

`uv` can be used as a `pip` replacement for installing, uninstalling, and managing packages.

### `uv pip install`

This command is used to install packages.

**Install a package:**

```bash
uv pip install requests
```

**Install from a requirements file:**

```bash
uv pip install -r requirements.txt
```

**Install multiple packages:**

```bash
uv pip install "requests<3" "click>=8"
```

### `uv pip compile`

This command is used to compile a `pyproject.toml` or `requirements.in` file into a `requirements.txt` file.

**Compile `pyproject.toml` to `requirements.txt`:**

```bash
uv pip compile pyproject.toml -o requirements.txt
```

**Compile `requirements.in` to `requirements.txt`:**

```bash
uv pip compile requirements.in -o requirements.txt
```

### `uv venv`

This command is used to create and manage virtual environments.

**Create a virtual environment:**

```bash
uv venv
```

This will create a virtual environment in a `.venv` directory in the current folder.

**Create a virtual environment with a specific Python version:**

```bash
uv venv -p 3.9
```

### `uv tool install`

This command installs a tool from PyPI into an isolated, persistent virtual environment, and makes it available on your `PATH`.

**Install a tool:**

```bash
uv tool install ruff
```

### `uv tool run`

This command runs a tool in a temporary virtual environment. This is useful for tools that you don't need to have installed all the time.

**Run a tool:**

```bash
uv tool run black --check .
```

### `uv tool list`

This command lists all the tools you've installed with `uv tool install`.

```bash
uv tool list
```

### `uv tool uninstall`

This command uninstalls a tool that you previously installed with `uv tool install`.

```bash
uv tool uninstall ruff
```

### `uv init`

This command initializes a new Python project.

**Create a new project:**

```bash
uv init my-project
```

### `uv build`

This command builds a Python project into a wheel and a source distribution.

**Build a project:**

```bash
uv build
```

### `uv publish`

This command publishes a Python project to a package index.

**Publish a project:**

```bash
uv publish
```

### `uv run`

This command runs a command in the project's virtual environment.

**Run a command:**

```bash
uv run python my_script.py
```

### `uv lock`

This command creates a `uv.lock` file, which is a deterministic lock file of your project's dependencies.

**Create a lock file:**

```bash
uv lock
```

### `uv python`

This command allows you to manage Python installations.

**Install a Python version:**

```bash
uv python install 3.12
```

**List installed Python versions:**

```bash
uv python list
```
