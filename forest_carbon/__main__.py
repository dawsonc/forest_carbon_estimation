import combined_agb_calculator

# Working directory name
WORKING_DIRECTORY_NAME = (
    "/Users/jankahamori/Documents/robotics-88/forest_carbon_estimation"
)

# Path to the data to be augmented
PATH_TO_DATA = "/Users/jankahamori/Documents/robotics-88/forest_carbon_estimation/forest_carbon_estimation/example_data/10_trees.json"

# Path to where the file should be saved
SAVE_PATH = "/Users/jankahamori/Documents/robotics-88/forest_carbon_estimation/forest_carbon_estimation/forest_carbon"


def main():
    combined_agb_calculator.run_model(WORKING_DIRECTORY_NAME, PATH_TO_DATA, SAVE_PATH)


if __name__ == "__main__":
    main()
