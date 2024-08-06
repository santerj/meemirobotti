# meemirobotti

Generic template for new Python projects _with no dependencies!_.

## Which batteries are included

- basic project structure (source code, dependencies, tests) with minimal boilerplate
- nox sessions for testing, linting, auditing etc.
- TODO: tool configs in pyproject.toml
- TODO: basic Dockerfile
- TODO: Taskfile for recurring tasks (pip-compile etc.)

# Getting started

## Prerequisites

This project requires `Python 3.11+`.

## Installation

Clone this repository.

    git clone https://github.com/santerj/python-project-template.git [my-project]

## Usage

Run the interactive installer.

    python ./setup.py

After installation, there is some boilerplate code in `meemirootti/main.py` and `tests/test_main.py`.

Tasks for unit testing, linting, security auditing etc. are included in the `noxfile.py`. Try to invoke it with

    nox

If you don't have nox installed globally, just use the one included in the virtual environment:

    dev-venv/bin/nox
