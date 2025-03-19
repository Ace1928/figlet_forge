# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🌀 Figlet Forge - Eidosian Typography Engine
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# An advanced reimplementation of pyfiglet with colorized ANSI support,
# Unicode rendering, enhanced font ecosystem, and intelligent fallbacks.

.PHONY: all clean minimal full publish test lint format check docs security venv tox

all:
	@echo 'Figlet Forge: Enhanced Figlet System with colorized ANSI and Unicode support'
	@echo 'Run "make clean" to remove artifacts from previous builds'
	@echo 'Run "make minimal" to build a package with standard fonts only'
	@echo 'Run "make full" to build a complete package with all contributed fonts'
	@echo 'Run "make test" to run the test suite (use TEST_ARGS="..." for arguments)'
	@echo 'Run "make lint" to check code quality with ruff and mypy'
	@echo 'Run "make format" to format code according to project standards'
	@echo 'Run "make check" to run all pre-commit checks'
	@echo 'Run "make docs" to build documentation'
	@echo 'Run "make security" to run security scanners (bandit, safety)'
	@echo 'Run "make tox" to test across supported Python versions'
	@echo 'Run "make venv" to create a virtual environment for development'
	@echo 'Run "make publish" to upload to PyPI'

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf figlet_forge/fonts/
	rm -rf .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	mkdir -p figlet_forge/fonts/

minimal: clean
	cp figlet_forge/fonts-standard/* figlet_forge/fonts/
	python -m build

full: clean
	cp figlet_forge/fonts-standard/* figlet_forge/fonts/
	cp figlet_forge/fonts-contrib/* figlet_forge/fonts/
	python -m build

test:
	pytest tests/ $(TEST_ARGS)

test-cov:
	pytest tests/ --cov=figlet_forge --cov-report=html

lint:
	ruff figlet_forge/ tests/
	mypy figlet_forge/
	pyright figlet_forge/

format:
	black figlet_forge/ tests/
	isort figlet_forge/ tests/

check:
	pre-commit run --all-files

security:
	bandit -r figlet_forge/
	safety check

docs:
	cd docs && make html

tox:
	tox

venv:
	python -m venv .venv
	@echo "Virtual environment created at .venv/"
	@echo "Activate with: source .venv/bin/activate"
	@echo "Then install: pip install -e '.[dev,docs]'"

publish: check test security
	python -m build
	python -m twine check dist/*
	python -m twine upload dist/*
