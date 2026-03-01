# Product-base-Spec-Kit — local task runner
# Run `make help` to see available commands

PYTHON := python3
SHELL  := /bin/bash

.PHONY: help validate lint-docs lint-contracts check-trace check-all install-tools

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

validate: ## Validate all requirements.yml against JSON Schema
	@echo "==> Validating requirements.yml files..."
	@failed=0; \
	for f in $$(find initiatives -name requirements.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  check-jsonschema --schemafile tools/schemas/requirements.schema.json "$$f" || failed=1; \
	done; \
	exit $$failed

lint-docs: ## Lint YAML and Markdown files (warning mode)
	@echo "==> Linting YAML..."
	@yamllint -c .yamllint.yml . || true
	@echo "==> Linting Markdown..."
	@markdownlint-cli2 "**/*.md" "#node_modules" || true

lint-contracts: ## Validate OpenAPI and AsyncAPI contracts
	@echo "==> Linting OpenAPI contracts..."
	@failed=0; \
	for f in $$(find initiatives -name openapi.yaml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  redocly lint "$$f" || failed=1; \
	done; \
	echo "==> Linting AsyncAPI contracts..."; \
	for f in $$(find initiatives -name asyncapi.yaml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  asyncapi validate "$$f" || failed=1; \
	done; \
	exit $$failed

check-trace: ## Check REQ-ID consistency (L3 requirements.yml <-> L4 trace.md)
	@echo "==> Checking REQ-ID consistency..."
	@$(PYTHON) tools/scripts/check-trace.py

check-all: validate lint-docs lint-contracts check-trace ## Run all validation checks
	@echo ""
	@echo "==> All checks complete"

install-tools: ## Install all required validation tools
	@echo "==> Installing Python tools..."
	pip install yamllint check-jsonschema pyyaml
	@echo "==> Installing Node.js tools..."
	npm install -g markdownlint-cli2 @redocly/cli @asyncapi/cli
	@echo "==> Note: install oasdiff from https://github.com/oasdiff/oasdiff"
