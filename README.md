# Forest Carbon Estimation 🌲🌳💨

This repository contains code for estimating the above-ground biomass carbon in forests, using a database that identifies the linear regression parameters for the biomass according the tree's taxa, group, and specific gravity.

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

## Files

- `/example_data`: 
    - This folder contains generated data samples on 10, 100, and 1000 trees. 
    - The data for each tree include: 
        - `dbh`: this stands for the diameter at breast height, which is 4.5 feet above the ground
        - `species`: in our sample data, the species we include are `Ash`, `Maple`, `Oaks`, and `Pine, lodgepole`
        - `x_pos`
        - `y_pos`
- `/scripts`:
    - `generate_test_data.py`: this is the script used to generate the data in `/example_data`
- `/forest_carbon`:
    - This folder includes the models that we developed to estimate the biomass of individual trees
    - `/data`: this includes data on different species of trees, such as wood specific gravity, which we use to determine parameters to our model
    - `abg_biomass.py`: this file contains functions for calculating the above-ground biomass (AGB) of individual trees using a linear regression model with arguments based on the tree's species, DBH, and other parameters.
    - `combined_agb_calculator.py`: this script combines multiple AGB calculation methods and provides a unified interface to estimate the biomass of trees using different models based on what information is known about the tree.
    - `single_tree_estimation.py`: this script is another method for estimating the biomass of a single tree, which uses different parameters for an exponential model.
    - `tree_preprocessing.py`: this includes functions for preprocessing tree data, such as cleaning, normalizing, and preparing the data for biomass estimation models.
- `/notebooks`:
    - `kriging.ipynb`: this is a notebook that visualizes the data in a forest and implements an ordinary kriging model to predict the DBH of trees in the forest.
- `/tests`: 
    - This folder contains unittests for our biomass calculations.