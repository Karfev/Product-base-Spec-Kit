# Product-base-Spec-Kit — local task runner
# Run `make help` to see available commands

PYTHON := python3
SHELL  := /bin/bash

TEST_UNIT_CMD ?= echo "Set TEST_UNIT_CMD, e.g. 'pytest -m unit'" && exit 1
TEST_CONTRACT_CMD ?= echo "Set TEST_CONTRACT_CMD, e.g. 'pytest -m contract'" && exit 1
TEST_INTEGRATION_CMD ?= echo "Set TEST_INTEGRATION_CMD, e.g. 'pytest -m integration'" && exit 1
TEST_PERF_CMD ?= echo "Set TEST_PERF_CMD, e.g. 'k6 run tests/perf/smoke.js'" && exit 1

.PHONY: help validate validate-services validate-registry lint-docs lint-contracts check-trace check-spec-quality check-release-rollout check-all collect-evidence install-tools test-unit test-contract test-integration test-perf

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

validate: ## Validate all requirements.yml against JSON Schema
	@echo "==> Validating requirements.yml files..."
	@failed=0; \
	for f in $$(find initiatives -name requirements.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/requirements.schema.json "$$f" || failed=1; \
	done; \
	exit $$failed

validate-services: ## Validate all machine-readable service artifacts against JSON Schema (L2.5)
	@echo "==> Validating service requirements.yml files..."
	@failed=0; \
	for f in $$(find services -name requirements.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/service-requirements.schema.json "$$f" || failed=1; \
	done; \
	echo "==> Validating incident-catalog.yml files..."; \
	for f in $$(find services -name incident-catalog.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/incident-catalog.schema.json "$$f" || failed=1; \
	done; \
	echo "==> Validating request-catalog.yml files..."; \
	for f in $$(find services -name request-catalog.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/request-catalog.schema.json "$$f" || failed=1; \
	done; \
	echo "==> Validating change-catalog.yml files..."; \
	for f in $$(find services -name change-catalog.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/change-catalog.schema.json "$$f" || failed=1; \
	done; \
	echo "==> Validating billing/parameters.yml files..."; \
	for f in $$(find services -path '*/billing/parameters.yml' | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/billing-parameters.schema.json "$$f" || failed=1; \
	done; \
	echo "==> Validating responsibilities.yml files..."; \
	for f in $$(find services -name responsibilities.yml | grep -v '{'); do \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/responsibilities.schema.json "$$f" || failed=1; \
	done; \
	exit $$failed

validate-registry: ## Validate all products/*/requirements-registry.yml against JSON Schema
	@echo "==> Validating requirements-registry.yml files..."
	@failed=0; \
	found=0; \
	for f in $$(find products -name requirements-registry.yml | grep -v '{'); do \
	  found=1; \
	  echo "  Checking $$f"; \
	  python3 -m check_jsonschema --schemafile tools/schemas/requirements-registry.schema.json "$$f" || failed=1; \
	done; \
	if [ "$$found" -eq 0 ]; then echo "  No requirements-registry.yml files found — skipping"; fi; \
	exit $$failed

lint-docs: ## Lint YAML and Markdown files (warning mode)
	@echo "==> Linting YAML..."
	@command -v yamllint >/dev/null 2>&1 && yamllint -c .yamllint.yml . || echo "  yamllint not found — run: make install-tools"
	@echo "==> Linting Markdown..."
	@markdownlint-cli2 "**/*.md" "#node_modules" "#.claude" "#.planning" || true

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

check-spec-quality: ## Check .specify specs quality gates
	@echo "==> Checking .specify specs quality..."
	@$(PYTHON) tools/scripts/check-spec-quality.py

check-release-rollout: ## Validate rollout/migration consistency vs ops/slo.yaml + ops/prr-checklist.md
	@echo "==> Checking release rollout consistency..."
	@$(PYTHON) tools/scripts/check-release-rollout.py

collect-evidence: ## Collect GSD execution evidence into RTM report
	@echo "==> Collecting evidence from .planning/ SUMMARY files..."
	@$(PYTHON) tools/scripts/collect-evidence.py

test-unit: ## Run unit tests (override TEST_UNIT_CMD)
	@bash -lc '$(TEST_UNIT_CMD)'

test-contract: ## Run contract tests (override TEST_CONTRACT_CMD)
	@bash -lc '$(TEST_CONTRACT_CMD)'

test-integration: ## Run integration tests (override TEST_INTEGRATION_CMD)
	@bash -lc '$(TEST_INTEGRATION_CMD)'

test-perf: ## Run performance tests (override TEST_PERF_CMD)
	@bash -lc '$(TEST_PERF_CMD)'

check-all: validate validate-services validate-registry lint-docs lint-contracts check-trace check-spec-quality ## Run all validation checks
	@echo ""
	@echo "==> All checks complete"

install-tools: ## Install all required validation tools
	@echo "==> Installing Python tools..."
	pip install yamllint check-jsonschema pyyaml
	@echo "==> Installing Node.js tools..."
	npm install -g markdownlint-cli2 @redocly/cli @asyncapi/cli
	@echo "==> Note: install oasdiff from https://github.com/oasdiff/oasdiff"
