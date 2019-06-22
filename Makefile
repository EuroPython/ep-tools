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
	@echo "install-dev - install in development mode"
	@echo "tag - create a git tag with current version"

install:
	pip install -U pip setuptools pipenv
	pipenv install
	python setup.py install

install-dev:
	pip install -U pip setuptools pipenv
	pipenv install --dev
	python setup.py develop

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	pyclean .
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.log*' -delete
	find . -name '.DS_Store' -delete

lint:
	flake8 $(project-name)

format:
	black --line-length=120 --safe .

pre-commit:
	pre-commit run

tag: clean
	@echo "Creating git tag v$(version)"
	git tag v$(version)
	git push --tags

badges:
	inv fetch-talks-json -c ep2018 -o notebooks/talks.json -s accepted
	inv fetch-ticket-profiles -c ep2018 -o notebooks/profiles.json
  	python eptools/badge_creator.py
