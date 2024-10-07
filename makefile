VENV_DIR = venv
REQ_FILE = requirements.txt

# Default target
.PHONY: help venv-commands deps-commands setup-venv delete-venv install-deps export-deps list-deps port-forward

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
