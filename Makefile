# =============================================================================
# Makefile - Weather DataOps Platform
# =============================================================================

.PHONY: setup-python clean test lint dagster-dev infra-init infra-plan infra-apply infra-destroy

# -----------------------------------------------------------------------------
# Python Setup
# -----------------------------------------------------------------------------

setup-python:
	python -m venv .venv
	./.venv/Scripts/pip install -r requirements.txt

# -----------------------------------------------------------------------------
# Testing & Linting
# -----------------------------------------------------------------------------

test:
	./.venv/Scripts/pytest ingestion/tests -v

lint:
	./.venv/Scripts/ruff check .

lint-fix:
	./.venv/Scripts/ruff check --fix .

# -----------------------------------------------------------------------------
# Dagster (Orchestration)
# -----------------------------------------------------------------------------

dagster-dev:
	cd orchestration && ../.venv/Scripts/dagster dev

# -----------------------------------------------------------------------------
# dbt (Transformation)
# -----------------------------------------------------------------------------

dbt-run:
	cd transformations && ../.venv/Scripts/dbt run --profiles-dir .

dbt-test:
	cd transformations && ../.venv/Scripts/dbt test --profiles-dir .

dbt-docs:
	cd transformations && ../.venv/Scripts/dbt docs generate --profiles-dir .

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean:
	Remove-Item -Recurse -Force -ErrorAction SilentlyContinue __pycache__, .terraform, .venv

# -----------------------------------------------------------------------------
# Infrastructure (Terraform)
# -----------------------------------------------------------------------------

infra-init:
	cd infra && terraform init

infra-plan:
	cd infra && terraform plan

infra-apply:
	cd infra && terraform apply

infra-destroy:
	cd infra && terraform destroy
