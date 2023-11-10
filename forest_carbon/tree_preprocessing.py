"""Pre-process tree measurements to make AGB estimation easier."""
import pandas as pd


def create_common_name_dictionary(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Initialize an empty dictionary to store the data
    common_name_data = {}

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        common_name = row["Common name"]
        taxa = row["Taxa"].split()[0]  # Extract the first word from 'Taxa'
        fia_species = row["FIA species code"]
        wood_specific_gravity = row["Wood specific gravity"]
        group = row["Group"]

        # Add an entry to the dictionary
        common_name_data[common_name] = {
            "taxa": taxa,
            "fia_species_code": fia_species,
            "spg": wood_specific_gravity,
            "group": group,
        }

    return common_name_data


def preprocess_tree_entry(tree: dict, database: dict) -> dict:
    """Preprocess a tree entry to add information on the taxa, group, etc.

    Args:
        tree (dict): A dictionary containing information on a single tree. Should
            include a "species" tag with a label for the species.
        database (dict): A dictionary containing information on the species, generated
            by the `create_common_name_dictionary` function.

    Returns:
        dict: The input dictionary with additional information added on taxa, group,
            and specific gravity.

    Raises:
        KeyError: If the species label is not found in the common name dictionary.
    """
    # Extract the species label
    species = tree["species"]

    # Extract the data from the database
    taxa = database[species]["taxa"]
    group = database[species]["group"]
    spg = database[species]["spg"]
    fia_species_code = database[species]["fia_species_code"]

    # Add the data to the tree dictionary
    tree["taxa"] = taxa
    tree["group"] = group
    tree["spg"] = spg
    tree["fia_species_code"] = fia_species_code

    return tree


def preprocess_tree_entries(trees: list, database: dict) -> list:
    """Preprocess a list of tree entries.

    Args:
        trees (list): A list of dictionaries containing information on trees. Each
            dictionary should include a "species" tag with a label for the species.
        database (dict): A dictionary containing information on the species, generated
            by the `create_common_name_dictionary` function.

    Returns:
        list: The input list with additional information added on taxa, group,
            and specific gravity.

    Raises:
        KeyError: If the species label of any tree is not found in the common name
            dictionary.
    """
    return [preprocess_tree_entry(tree, database) for tree in trees]
