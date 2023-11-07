import json
from beartype import beartype
from beartype.typing import Callable, TypeAlias
import math

AGBModel: TypeAlias = Callable[[float, float, float], float]

@beartype
def load_tree_data_from_json(
    file_path: str)-> list:
    """
    Function to load JSON data from a file
    """
    tree_data = []

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            # Check if the JSON file contains the "trees" key
            if "trees" in data:
                trees = data["trees"]

                for tree_info in trees:
                    # Extract relevant information
                    dbh = tree_info.get("dbh")
                    species = tree_info.get("species")
                    x_pos = tree_info.get("x_pos")
                    y_pos = tree_info.get("y_pos")

                    # Create a dictionary for each tree
                    tree = {
                        "dbh": dbh,
                        "species": species,
                        "x_pos": x_pos,
                        "y_pos": y_pos
                    }

                    tree_data.append(tree)

                return tree_data

            else:
                print("JSON file does not contain the 'trees' key.")
                return None

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None

def choosing_the_model() -> AGBModel:
    """
    Function to decide which model to use and create the actual model.
    """
    # Chek if relevant tree type

    # Check if we have tree height

    #Search for e

    pass