VENV_DIR = venv
REQ_FILE = requirements.txt

# Default target
.PHONY: help venv-commands deps-commands setup-venv delete-venv install-deps export-deps list-deps port-forward alembic-commands upgrade-db downgrade-db create-migration

help:
	@echo "Makefile usage:"
	@echo ""
	@echo "Virtual environment commands:"
	@echo "  make setup-venv         - Create a Python virtual environment in the 'venv' directory."
	@echo "  make delete-venv        - Remove the virtual environment."
	@echo ""
	@echo "Dependency management commands:"
	@echo "  make install-deps       - Install dependencies from requirements.txt inside the virtual environment."
	@echo "  make export-deps        - Export installed dependencies to requirements.txt."
	@echo "  make list-deps          - List all installed dependencies."
	@echo ""
	@echo "Alembic migration commands:"
	@echo "  make create-migration   - Create a new Alembic migration with a message."
	@echo "  make upgrade-db         - Apply Alembic migrations (upgrade)."
	@echo "  make downgrade-db       - Revert Alembic migrations (downgrade)."
	@echo ""
	@echo "Port forwarding commands:"
	@echo "  make port-forward       - Export port 8000 to 'bookly' via serveo.net."
	@echo ""
	@echo "  make help               - Show this help message."

# Group venv related commands
venv-commands: setup-venv delete-venv

# Create a virtual environment
setup-venv:
	python -m venv $(VENV_DIR)

# Remove the virtual environment
delete-venv:
	rm -rf $(VENV_DIR)

# Group dependency related commands
deps-commands: install-deps export-deps list-deps

# Install dependencies from the requirements.txt file
install-deps: $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQ_FILE)

# Export installed dependencies to the requirements.txt file
export-deps: $(VENV_DIR)
	$(VENV_DIR)/bin/pip freeze > $(REQ_FILE)

# List all installed dependencies
list-deps: $(VENV_DIR)
	$(VENV_DIR)/bin/pip freeze

# Port forwarding command
port-forward:
	ssh -R bookly:80:localhost:8000 serveo.net

# Group Alembic related commands
alembic-commands: upgrade-db downgrade-db create-migration

# Create a new Alembic migration with a message
create-migration: $(VENV_DIR)
	$(VENV_DIR)/bin/alembic revision -m "$(message)"

# Apply Alembic migrations (upgrade)
upgrade-db: $(VENV_DIR)
	$(VENV_DIR)/bin/alembic upgrade head

# Revert Alembic migrations (downgrade)
downgrade-db: $(VENV_DIR)
	$(VENV_DIR)/bin/alembic downgrade -1
