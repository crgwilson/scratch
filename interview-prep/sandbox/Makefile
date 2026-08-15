PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin
.DEFAULT_GOAL := help

.PHONY: venv test test-bst test-cloud-sync test-doubly-linked-list test-extended-lru-cache test-ip-address-iterator test-job-scheduler test-max-heap test-mini-sql test-rate-limiter test-refactoring-drill test-resumable-iterator test-singly-linked-list test-stdlib-drills test-time-kv reset clean help

venv: ## Bootstrap your venv
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e ".[test]"

test: venv ## Run pytest
	$(BIN)/pytest

test-singly-linked-list: venv ## Run singly linked list tests
	$(BIN)/pytest tests/test_singly_linked_list.py

test-doubly-linked-list: venv ## Run doubly linked list tests
	$(BIN)/pytest tests/test_doubly_linked_list.py

test-max-heap: venv ## Run max heap tests
	$(BIN)/pytest tests/test_max_heap.py

test-bst: venv ## Run binary search tree tests
	$(BIN)/pytest tests/test_binary_search_tree.py

test-time-kv: venv ## Run time-based key/value store tests
	$(BIN)/pytest tests/test_time_based_kv_store.py

test-resumable-iterator: venv ## Run resumable iterator tests
	$(BIN)/pytest tests/test_resumable_iterator.py

test-rate-limiter: venv ## Run rate limiter tests
	$(BIN)/pytest tests/test_rate_limiter.py

test-extended-lru-cache: venv ## Run extended LRU cache tests
	$(BIN)/pytest tests/test_extended_lru_cache.py

test-mini-sql: venv ## Run mini SQL tests
	$(BIN)/pytest tests/test_mini_sql.py

test-cloud-sync: venv ## Run cloud sync tests
	$(BIN)/pytest tests/test_cloud_sync.py

test-job-scheduler: venv ## Run job scheduler tests
	$(BIN)/pytest tests/test_job_scheduler.py

test-ip-address-iterator: venv ## Run IP address iterator tests
	$(BIN)/pytest tests/test_ip_address_iterator.py

test-refactoring-drill: venv ## Run refactoring drill characterization tests
	$(BIN)/pytest tests/test_refactoring_drill.py

test-stdlib-drills: venv ## Run standard-library drills
	$(BIN)/pytest tests/test_stdlib_drills.py

clean: ## Cleanup cache files such as pycache, pyc, etc
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -prune -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

reset: clean ## Reset the sandbox back to the defaults.
	find src -mindepth 1 ! -name ".gitkeep" -exec rm -rf {} +
	find tests -mindepth 1 ! -name ".gitkeep" -exec rm -rf {} +
	cp -R reset_templates/src/. src/
	cp -R reset_templates/tests/. tests/
	rm -rf $(VENV)

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
