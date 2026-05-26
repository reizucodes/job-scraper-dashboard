BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: help setup setup-backend setup-frontend setup-backend-clean setup-frontend-clean fresh-install reset-db clean-backend clean-frontend backend-dev frontend-dev test-backend test-frontend build-frontend

help:
	@echo "Available commands:"
	@echo "  make setup            - Install backend + frontend dependencies"
	@echo "  make setup-backend    - Create backend venv and install backend deps"
	@echo "  make setup-frontend   - Install frontend deps"
	@echo "  make fresh-install    - Reset backend/frontend install artifacts and reinstall"
	@echo "  make reset-db         - Remove local SQLite database file"
	@echo "  make clean-backend    - Remove backend venv, DB, and Python caches"
	@echo "  make clean-frontend   - Remove frontend node_modules, dist, and coverage"
	@echo "  make backend-dev      - Run backend API server"
	@echo "  make frontend-dev     - Run frontend dev server"
	@echo "  make test-backend     - Run backend tests"
	@echo "  make test-frontend    - Run frontend tests"
	@echo "  make build-frontend   - Run frontend typecheck + production build"

setup: setup-backend setup-frontend

setup-backend:
	cd $(BACKEND_DIR) && python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e '.[dev]' && alembic upgrade head

setup-frontend:
	cd $(FRONTEND_DIR) && npm install

fresh-install: clean-backend clean-frontend setup

reset-db:
	rm -f $(BACKEND_DIR)/job_scraper_dashboard.db

clean-backend: reset-db
	rm -rf $(BACKEND_DIR)/.venv $(BACKEND_DIR)/.pytest_cache $(BACKEND_DIR)/.ruff_cache $(BACKEND_DIR)/.mypy_cache $(BACKEND_DIR)/__pycache__ $(BACKEND_DIR)/*.egg-info

clean-frontend:
	rm -rf $(FRONTEND_DIR)/node_modules $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/coverage

backend-dev:
	cd $(BACKEND_DIR) && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000

frontend-dev:
	cd $(FRONTEND_DIR) && npm run dev

test-backend:
	cd $(BACKEND_DIR) && . .venv/bin/activate && pytest

test-frontend:
	cd $(FRONTEND_DIR) && npm run test

build-frontend:
	cd $(FRONTEND_DIR) && npm run build
