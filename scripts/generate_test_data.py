"""A script for generating random example data in the R88 format."""
import json
import random


def generate_tree_example():
    """Generate a random tree example."""
    dbh = round(random.uniform(0.2, 0.5), 3)
    species = random.choice(["ash tree", "oak tree", "maple tree", "pine tree"])
    x_pos = round(random.uniform(30, 40), 6)
    y_pos = round(random.uniform(-10, 0), 6)

    tree = {"dbh": dbh, "species": species, "x_pos": x_pos, "y_pos": y_pos}

    return tree


def generate_json_examples(num_examples):
    """Generate a list of random tree examples."""
    trees = [generate_tree_example() for _ in range(num_examples)]
    data = {"trees": trees}
    json_data = json.dumps(data, indent=2)
    return json_data


if __name__ == "__main__":
    # Generate some examples and save to a file
    num_examples = 100
    json_examples = generate_json_examples(num_examples)

    with open(f"data/{num_examples}_trees.json", "w") as f:
        f.write(json_examples)
