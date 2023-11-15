import json
import os
import config, abg_biomass, single_tree_estimation, tree_preprocessing


def load_tree_data_from_json(
    data_path: str,
    csv_file_path: str)-> list:
    """
    Function to load JSON data from a file
    """
    tree_data = []
    

    try:
        with open(data_path, 'r') as json_file:
            data = json.load(json_file)
            database = tree_preprocessing.create_common_name_dictionary(csv_file_path)
            tree = tree_preprocessing.preprocess_tree_entries(trees=data['trees'], database=database)

            # Check if the JSON file contains the "trees" key
            for tree_info in tree:
                # Extract relevant information
                dbh = tree_info.get("dbh")
                group = tree_info.get("group")
                taxa = tree_info.get("taxa")
                x_pos = tree_info.get("x_pos")
                y_pos = tree_info.get("y_pos")
                spg = tree_info.get("spg")

                    # Create a dictionary for each tree
                tree = {
                        "dbh": dbh,
                        "group": group,
                        "taxa": taxa,
                        "x_pos": x_pos,
                        "y_pos": y_pos,
                        "height": None,
                        "spg": spg,
                    }

                tree_data.append(tree)

            return tree_data

    except FileNotFoundError:
        print(f"File not found: {data_path}")
        return None

    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None


def choosing_the_model(group, taxa, dbh, spg, height, df, model_height, model_no_height) -> float:
    """
    Function to decide which model to use and create the actual model.
    The environmental variable E can be modified, or the generic value from the config file can be used
    """

    results = abg_biomass.abg_biomass_model(group, taxa, spg, df)

    if results:
        b0, b1, Rsquared, diameterClass = results
        biomass = abg_biomass.biomass(b0, b1, diameterClass, dbh)
    elif height:
        biomass = single_tree_estimation.apply_AGB_model(model_height, spg, dbh, height)
    else:
        biomass = single_tree_estimation.apply_AGB_model_no_height(model_no_height, spg, dbh, config.E)
    return biomass


def apply_model():
    """
    Takes the chosen model, the name of the model, and applies it to the data
    """
    tree_data = load_tree_data_from_json(config.PATH_TO_DATA, config.PATH_TO_CSV)

    # Checking if the inputted data was valid
    if tree_data is None:
        return None

    df = abg_biomass.load_taxa_agb_model_data(config.PATH_TO_TAXA_LEVEL_ABG_MODEL_PARAMETERS)
    model_height = single_tree_estimation.create_AGB_function(coef = config.COEF, exp = config.EXP)
    model_no_height = single_tree_estimation.create_AGB_function_no_height(const=config.CONST, coef_e=config.COEF_E, coef_rho=config.COEF_RHO, coef_d=config.COEF_D, coef_d_squared=config.COEF_D_SQUARED)

    for tree in tree_data:
        group = tree["group"]
        taxa = tree["taxa"]
        dbh = tree["dbh"]
        spg=tree["spg"]
        height = tree["height"]

        #Choosing the best available model for the given parameters 
        biomass = choosing_the_model(group=group, taxa=taxa, dbh=dbh, spg=spg, height=height,df=df, model_height=model_height, model_no_height=model_no_height)
        tree["ABG value"] = biomass
        
    return tree_data

def save_model(save_path = config.SAVE_PATH):
    processed_data = apply_model()

    path = os.path.join(save_path, "processed_data.json")
    with open(path, 'w') as json_file:
        json.dump(processed_data, json_file, indent=2)
    
    print(f"Data saved")

    return

save_model()
