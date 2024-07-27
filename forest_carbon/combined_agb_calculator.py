import json
from typing import Callable, Optional

from beartype import beartype

from . import agb_biomass, config, single_tree_estimation, tree_preprocessing

AGBModel = Callable[[float, float, float], float]


@beartype
def load_tree_data_from_json(
    data_path: str, preprocessing_species_info_path: str
) -> Optional[list]:
    """
    Load tree data from a JSON file and preprocess it.

    Args:
    - data_path (str): Path to the JSON file.
    - csv_file_path (str): Path to the CSV file.

    Returns:
    List: Processed tree data, or None if no tree data is found.
    """
    tree_data = []

    try:
        with open(data_path, "r") as json_file:
            data = json.load(json_file)

            database = tree_preprocessing.create_common_name_dictionary(
                preprocessing_species_info_path
            )
            tree = tree_preprocessing.preprocess_tree_entries(
                trees=data["trees"], database=database
            )

            for tree_info in tree:
                dbh, group, taxa, x_pos, y_pos, spg = (
                    tree_info.get("dbh"),
                    tree_info.get("group"),
                    tree_info.get("taxa"),
                    tree_info.get("x_pos"),
                    tree_info.get("y_pos"),
                    tree_info.get("spg"),
                )

                tree_dict = {
                    "dbh": dbh,
                    "group": group,
                    "taxa": taxa,
                    "x_pos": x_pos,
                    "y_pos": y_pos,
                    "height": None,
                    "spg": spg,
                }

                tree_data.append(tree_dict)

            return tree_data

    except FileNotFoundError:
        print(f"File not found: {data_path}")
        return None

    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None


@beartype
def choosing_the_model(
    group: str,
    taxa: str,
    dbh: float,
    spg: float,
    height,
    df,
    model_height: Optional[AGBModel],
    model_no_height: Optional[AGBModel],
) -> float:
    """
    Decide which model to use and apply it to estimate AGB.

    Args:
    - group (str): The group of the tree.
    - taxa (str): The taxa of the tree.
    - dbh (float): Diameter at breast height.
    - spg (float): Specific gravity of the tree.
    - height (float): The height of the tree.
    - df: DataFrame called by the function load_taxa_agb_model_data.
    - model_height (AGBModel): Model for estimating AGB when tree height is available.
    - model_no_height (AGBModel): Model for estimating AGB when tree height is not available.

    Returns:
    float: Estimated Above-Ground Biomass (AGB).
    """

    # If the tree species is known, use the most accurate model that estimates biomass
    # based on the species of the tree (tree_group, tree_taxa)
    species_result = agb_biomass.agb_biomass_model(group, taxa, spg, df)
    if species_result:
        if isinstance(species_result, dict):
            b0, b1, Rsquared, diameterClass = list(species_result.values())[0]
        else:
            b0, b1, Rsquared, diameterClass = species_result
        biomass = agb_biomass.biomass(b0, b1, diameterClass, dbh)

    # If the tree has a given height but the species is not in our database, use a more generic model
    # based on the tree's height; it does not require knowledge of the specific species.
    elif height:
        biomass = single_tree_estimation.apply_AGB_model(model_height, spg, dbh, height)

    # If no information is available, use the most generic and less accurate model,
    # estimating biomass based on environmental variables specific to the region.
    else:
        biomass = single_tree_estimation.apply_AGB_model_no_height(
            model_no_height, spg, dbh, config.E
        )

    return biomass


@beartype
def apply_model(tree_data, path_to_taxa_level_parameters: str) -> Optional[list]:
    """
    Apply the best model available for each tree data.

    Args:
    - path_to_data (str): Path to the data to augment with AGB value.
    - path_to_csv (str): Path to the CSV file.

    Returns:
    dict: Augmented tree data with AGB values.
    """

    if tree_data is None:
        return None

    df = agb_biomass.load_taxa_agb_model_data(path_to_taxa_level_parameters)
    model_height = single_tree_estimation.create_AGB_function(
        coef=config.COEF, exp=config.EXP
    )
    model_no_height = single_tree_estimation.create_AGB_function_no_height(
        const=config.CONST,
        coef_e=config.COEF_E,
        coef_rho=config.COEF_RHO,
        coef_d=config.COEF_D,
        coef_d_squared=config.COEF_D_SQUARED,
    )

    for tree in tree_data:
        group, taxa, dbh, spg, height = (
            tree["group"],
            tree["taxa"],
            tree["dbh"],
            tree["spg"],
            tree["height"],
        )

        biomass = choosing_the_model(
            group=group,
            taxa=taxa,
            dbh=dbh,
            spg=spg,
            height=height,
            df=df,
            model_height=model_height,
            model_no_height=model_no_height,
        )
        tree["AGB value"] = biomass

    return tree_data


@beartype
def run_model(input_data_path: str, save_output_path: str):
    """
    Save the augmented data to the specified path.

    Args:
    - input_data_path (str): Path to the input data.
    - save_output_path (str): Path where the augmented data should be saved.
    """
    # Loading the tree data and preprocessing it
    preprocessing_species_info_path = config.PATH_TO_TREE_PREPROCESSING_SPECIES_INFO
    path_to_taxa_level_parameters = config.PATH_TO_TAXA_LEVEL_AGB_MODEL_PARAMETERS
    print(input_data_path)
    print(preprocessing_species_info_path)
    tree_data = load_tree_data_from_json(
        input_data_path, preprocessing_species_info_path
    )

    # Augmenting the tree data with Above-Ground Biomass (AGB) information
    processed_data = apply_model(tree_data, path_to_taxa_level_parameters)

    # Saving the augmented tree data into a new file
    with open(save_output_path, "w") as json_file:
        json.dump(processed_data, json_file, indent=2)

    print("Augmented data saved successfully.")
