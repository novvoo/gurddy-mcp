# Makefile for MCP Server Development

.PHONY: help generate-schemas verify test clean install dev

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

generate-schemas:  ## Generate tool schemas from function signatures
	python scripts/generate_registry.py

verify:  ## Verify consistency between schemas and implementations
	python scripts/verify_consistency.py

test:  ## Run all tests
	python -m pytest tests/ -v

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

install:  ## Install dependencies
	pip install -r requirements.txt

build: ## Build package (run pre-build hooks, test, then build)
	python scripts/build_hook.py
	python -m pytest tests/ -v
	python -m build

publish-test: build  ## Build and publish to TestPyPI
	python scripts/build_and_publish.py --test

publish: build  ## Build and publish to PyPI
	python scripts/build_and_publish.py --prod

dev: install generate-schemas verify  ## Set up development environment

docker-build:  ## Build Docker image with auto-generated schemas (fast)
	docker build -t gurddy-mcp .

docker-build-full:  ## Build Docker image using complete build pipeline (slower but thorough)
	docker build -f Dockerfile.build -t gurddy-mcp:full .

docker-run:  ## Run Docker container
	docker run -p 8080:8080 gurddy-mcp

# Shortcuts
schemas: generate-schemas
check: verify