"""
A script for generating random example data in the R88 format.

Generates trees that have different species and diameters, but adds some spatial
structure so that they can be used as test cases for mapping algorithms.
"""
import json
import random

import numpy as np

# Species means are taken from this resource:
# https://www.fs.usda.gov/ne/newtown_square/publications/research_papers/pdfs/scanned/OCR/ne_rp649.pdf
TREE_SPECIES_MEAN_DBH = {
    "ash tree": 0.22,
    "maple tree": 0.21,
    "oak tree": 0.26,
    "pine tree": 0.24,
}


def random_tree_diameter(
    species: str, x_pos: float, y_pos: float, width: float = 12
) -> float:
    """
    Samples a random tree diameter based on the species and position.

    Trees have a mean diameter based on their species, then we increase or decrease
    that diameter by scaling based on Himmelblau's function (just a convenient shape;
    https://en.wikipedia.org/wiki/Himmelblau%27s_function)

    Args:
        species: the species of the tree
        x_pos: the x position (meters) of the tree
        y_pos: the y position (meters) of the tree
        width: the width and height of the plot

    Returns:
        a DBH measurement (diameter at breast height; meters) of the tree.

    Raises:
        KeyError if `species` is not in TREE_SPECIES_MEAN_DBH
    """
    # Get the mean DBH of the species
    mean_dbh = TREE_SPECIES_MEAN_DBH[species]

    # Scale the position by the width and re-normalize to [-6, 6] (the preferred range
    # for evaluating Himmelblau's function. The exact function isn't so important,
    # so I just picked one that has an interesting-enough shape to be a good test case
    # for mapping
    x = (x_pos - width / 2.0) / width * 12
    y = (y_pos - width / 2.0) / width * 12
    himmelblau_value = (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2

    # This function has quite a large range, so we'll scale it, use the sigmoid
    # function to constrain it to [0, 1], then shift it
    dbh_scale_factor = 1.8 - 1 / (1 + np.exp(-himmelblau_value / 100))

    # Scale the mean DBH by the scale factor, then sample a random diameter from a
    # normal distribution with that mean and 10% standard deviation
    dbh = np.random.normal(mean_dbh * dbh_scale_factor, 0.1 * mean_dbh)

    return dbh


def generate_tree_example(width: float = 12) -> dict:
    """Generate a random tree example.

    Samples a random species, position, and diameter.

    Args:
        width: the width and height of the plot

    Returns:
        a dictionary with the keys `dbh`, `species`, `x_pos`, and `y_pos`
    """
    # Sample a random position
    x_pos = random.uniform(0, width)
    y_pos = random.uniform(0, width)

    # Sample a random species
    species = random.choice(["ash tree", "oak tree", "maple tree", "pine tree"])

    # Sample a random diameter
    dbh = random_tree_diameter(species, x_pos, y_pos, width)

    tree = {
        "dbh": dbh,
        "species": species,
        "x_pos": x_pos,
        "y_pos": y_pos,
    }

    return tree


def generate_tree_examples(num_examples: int, width: float = 12):
    """Generate a list of random tree examples.

    Args:
        num_examples: the number of examples to generate
        width: the width and height of the plot

    Returns:
        A list of dictionaries for each randomly sampled tree
    """
    return [generate_tree_example(width) for _ in range(num_examples)]


if __name__ == "__main__":
    # Generate some examples and save to a file
    num_examples = 10000
    trees = generate_tree_examples(num_examples)

    data = {"trees": trees}
    json_data = json.dumps(data, indent=2)

    with open(f"data/{num_examples}_trees.json", "w") as f:
        f.write(json_data)
