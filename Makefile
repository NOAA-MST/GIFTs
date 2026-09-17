SHELL=/bin/sh
VENV=.gifts

.PHONY: all build dev lint test docs clean distclean

all: build

${VENV}:
	python3 -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip setuptools wheel build

build: ${VENV}
	source ${VENV}/bin/activate; python -m build

dev: ${VENV}
	source ${VENV}/bin/activate; pip install -e .[test]

lint: dev
	${VENV}/bin/flake8 gifts tests

test: dev
	${VENV}/bin/pytest --cov=gifts tests

docs: ${VENV}
	source ${VENV}/bin/activate; pip install -e .[docs]; sphinx-build -b html docs docs/_build/html

clean: distclean
	rm -rf ${VENV}
	find . -name '*.py[co~]' -exec rm -f {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +

distclean:
	find . -name '*.egg-info' -exec rm -rf {} +
	rm -rf .cache .eggs .pytest_cache build dist
