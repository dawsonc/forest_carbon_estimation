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


if __name__ == "__main__":
    # Example usage:
    csv_file = "forest_carbon/data/tree_species_info.csv"
    resulting_dictionary = create_common_name_dictionary(csv_file)

    # Print the resulting dictionary
    for common_name, data in resulting_dictionary.items():
        print(f"Common Name: {common_name}")
        print(f"Taxa: {data['taxa']}")
        print(f"Group: {data['group']}")
        print(f"FIA Species: {data['fia_species_code']}")
        print(f"Wood Specific Gravity: {data['spg']}")
        print("-" * 30)
