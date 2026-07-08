PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin

.PHONY: venv test reset clean help

venv: ## Bootstrap your venv
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e ".[test]"

test: venv ## Run pytest
	$(BIN)/pytest

clean: ## Cleanup cache files such as pycache, pyc, etc
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -prune -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

reset: clean ## Reset the sandbox back to the defaults.
	find src tests -mindepth 1 ! -name ".gitkeep" ! -path "src/sandbox.py" ! -path "tests/test_example.py" -exec rm -rf {} +
	rm -rf $(VENV)

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
