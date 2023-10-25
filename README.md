# Forest Carbon Estimation 🌲🌳💨

This repository contains code for estimating the above-ground biomass carbon in forests, using data collected from drones.

## Installation

This project uses [`poetry`](https://python-poetry.org/docs/) for dependency management. You can install poetry with the instructions [here](https://python-poetry.org/docs/#installation). To install this package and its dependencies, and initialize the development environment, run

```
poetry install
poetry run pre-commit install  # only needed for development
```

Poetry will create and manage a virtual environment for you, and it puts all of the dependency management under version control, (hopefully) leading to a more consistent install/development experience across team members.

To run a command in the poetry virtual environment, either run the command with poetry

```
poetry run <your command>  # e.g. poetry run python hello_world.py
```

or start a shell with the poetry environment activated

```
poetry shell
```

## Developing

This project uses [`ruff`](https://github.com/astral-sh/ruff) for linting and auto-formatting, `mypy` for type checking, and `pre-commit` for running code quality checks when you commit code.
