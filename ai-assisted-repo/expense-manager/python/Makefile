PYTEST ?= $(shell if [ -f .venv/bin/pytest ]; then echo ../.venv/bin/pytest; elif command -v pytest >/dev/null 2>&1; then echo pytest; elif python3 -m pytest --version >/dev/null 2>&1; then echo "python3 -m pytest"; else echo ""; fi)

.PHONY: all run test setup clean

all: test

run: test

test:
	@if [ -n "$(PYTEST)" ]; then \
		(cd expense-manager && $(PYTEST)); \
	else \
		echo "pytest not found. Running setup.sh to configure environment..."; \
		./setup.sh && (cd expense-manager && ../.venv/bin/pytest); \
	fi

setup:
	@./setup.sh

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf *.pyc
