.PHONY: help clean clean-pyc clean-build list test test-dbg test-cov test-all coverage docs release sdist install deps develop tag

project-name = eptools

version-var := "__version__ = "
version-string := $(shell grep $(version-var) $(project-name)/version.py)
version := $(subst __version__ = ,,$(version-string))

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-pyenv - remove the pipenv Python environment"
	@echo "lint - check style with flake8"
	@echo "install - install"
	@echo "develop - install in development mode"
	@echo "deps - install dependencies"
	@echo "tag - create a git tag with current version"

install: deps
	pipenv run python setup.py install

develop: dev_deps
	pipenv run python setup.py develop
	pipenv run pre-commit install

deps:
	pipenv install --skip-lock

dev_deps:
	pipenv install --skip-lock --dev

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.log*' -delete
	find . -name '.DS_Store' -delete

clean-pyenv:
	pipenv --rm

lint:
	pipenv run flake8 $(project-name) test

format:
	pipenv run black --line-length=120 --safe .

pre-commit:
	pipenv run pre-commit run

tag: clean
	@echo "Creating git tag v$(version)"
	git tag v$(version)
	git push --tags
