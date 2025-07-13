# Makefile for weather project

.PHONY: test test-coverage test-watch clean

# Run unit tests with coverage report
test:
	@echo "Running unit tests..."
	cd src && poetry run python -m pytest ../tests/ -v --tb=short --durations=10

# Run tests with coverage
test-coverage:
	@echo "Running unit tests with coverage..."
	cd src && poetry run python -m pytest ../tests/ -v --tb=short --cov=modules.weather --cov-report=html --cov-report=term-missing

# Run tests in watch mode (requires pytest-watch)
test-watch:
	@echo "Running tests in watch mode..."
	cd src && poetry run python -m pytest ../tests/ -f

# Clean test artifacts and temporary files
clean:
	@echo "Cleaning test artifacts and temporary files..."
	rm -rf src/htmlcov/
	rm -rf src/.coverage
	rm -rf .pytest_cache/
	rm -rf src/.pytest_cache/
	rm -rf tests/.pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage.*" -delete
	@echo "Cleanup completed!"
