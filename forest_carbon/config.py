import os

# Config for create_AGB_function
COEF = 0.0673
EXP = 0.976

# Config for create_AGB_function_no_height
CONST = 1.803
COEF_E = 0.976
COEF_RHO = 0.976
COEF_D = 2.673
COEF_D_SQUARED = 0.0299

# Environmental variable, to be changed to the relevant value based on the forest's position
E = 1.0

# Path to the CSV file used to augment the data with the group and taxa name
PATH_TO_TREE_PREPROCESSING_SPECIES_INFO = os.path.join(
    os.path.dirname(__file__), "data/tree_species_info.csv"
)

# Path to the file used in tree-specific biomass estimation
PATH_TO_TAXA_LEVEL_AGB_MODEL_PARAMETERS = os.path.join(
    os.path.dirname(__file__), "data/taxa_level_agb_model_parameters.csv"
)
