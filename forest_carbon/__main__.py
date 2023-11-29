from forest_carbon import combined_agb_calculator

# Path to the data to be augmented
PATH_TO_DATA = "./example_data/10_trees.json"

# Path to where the file should be saved
SAVE_PATH = "./example_data/10_trees_processed.json"


def main():
    combined_agb_calculator.run_model(PATH_TO_DATA, SAVE_PATH)


if __name__ == "__main__":
    main()
