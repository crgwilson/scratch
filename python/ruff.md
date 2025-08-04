# Ruff

Ruff is an extremely fast Python linter and code formatter, written in Rust. It can be used to check your code for errors, enforce coding standards, and automatically format your code.

## Installation

You can install `ruff` with `uv` or `pip`:

```bash
# With uv
uv tool install ruff

# With pip
pip install ruff
```

## Common Commands

### `ruff check`

This command checks your code for errors and violations of coding standards.

**Check the current directory:**

```bash
ruff check .
```

**Automatically fix fixable errors:**

```bash
ruff check . --fix
```

### `ruff format`

This command formats your code according to the configured style.

**Format the current directory:**

```bash
ruff format .
```

### `ruff rule`

This command allows you to view information about the linter rules.

**List all rules:**

```bash
ruff rule --all
```

**Show information about a specific rule:**

```bash
ruff rule F841
```

### `ruff clean`

This command clears the ruff cache.

```bash
ruff clean
```

### Watch Mode

Ruff can be run in a watch mode, where it will automatically re-run when files are changed.

```bash
ruff check . --watch
```

## Configuration

Ruff is configured in the `pyproject.toml` file, under the `[tool.ruff]` section.

```toml
[tool.ruff]
# Set the line length
line-length = 88

# Enable Pyflakes and pycodestyle rules
[tool.ruff.lint]
select = ["E", "F"]

# Ignore unused variable warnings
ignore = ["F841"]

# Configure the formatter
[tool.ruff.format]
quote-style = "double"
```

### Common Rule Sets

*   `E`/`W`: pycodestyle (Errors and Warnings)
*   `F`: Pyflakes
*   `I`: isort
*   `B`: flake8-bugbear
*   `A`: flake8-builtins
