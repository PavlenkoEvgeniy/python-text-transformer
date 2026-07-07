.PHONY: help test install-dev pyinstaller clean

help:
	@echo "Text Transformer Pro - Build Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install-dev    - Install package in development mode with test deps"
	@echo "  make test          - Run tests with coverage"
	@echo "  make pyinstaller   - Build standalone executable"
	@echo "  make clean         - Clean build artifacts"

install-dev:
	pip install -e ".[dev]"

test:
	PYTHONPATH=src pytest tests/ -v --cov=src --cov-report=term-missing

pyinstaller:
	PYTHONPATH=src pyinstaller --onefile --windowed --name TextTransformer main.py

clean:
	rm -rf build dist *.spec
	rm -rf __pycache__ src/**/__pycache__ tests/__pycache__
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete