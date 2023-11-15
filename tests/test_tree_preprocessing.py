import unittest

import pandas as pd

from forest_carbon.tree_preprocessing import (
    create_common_name_dictionary,
    preprocess_tree_entries,
    preprocess_tree_entry,
)


class TestTreeProcessing(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        data = {
            "Common name": ["Oak", "Pine", "Maple"],
            "Taxa": ["Genus1 species1", "Genus2 species2", "Genus3 species3"],
            "FIA species code": [101, 102, 103],
            "Wood specific gravity": [0.6, 0.5, 0.7],
            "Group": ["GroupA", "GroupB", "GroupC"],
        }
        self.df = pd.DataFrame(data)
        self.csv_file = "test_data.csv"
        self.df.to_csv(self.csv_file, index=False)

        # Create a common name dictionary
        self.common_name_dict = create_common_name_dictionary(self.csv_file)

    def tearDown(self):
        # Clean up by removing the test CSV file
        import os

        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_create_common_name_dictionary(self):
        self.assertEqual(len(self.common_name_dict), 3)
        self.assertEqual(self.common_name_dict["Oak"]["taxa"], "Genus1")
        self.assertEqual(self.common_name_dict["Pine"]["fia_species_code"], 102)
        self.assertEqual(self.common_name_dict["Maple"]["spg"], 0.7)
        self.assertEqual(self.common_name_dict["Pine"]["group"], "GroupB")

    def test_preprocess_tree_entry(self):
        tree = {"species": "Oak"}
        result_tree = preprocess_tree_entry(tree, self.common_name_dict)
        self.assertEqual(result_tree["taxa"], "Genus1")
        self.assertEqual(result_tree["fia_species_code"], 101)
        self.assertEqual(result_tree["spg"], 0.6)
        self.assertEqual(result_tree["group"], "GroupA")

    def test_preprocess_tree_entries(self):
        trees = [{"species": "Pine"}, {"species": "Maple"}]
        result_trees = preprocess_tree_entries(trees, self.common_name_dict)
        self.assertEqual(result_trees[0]["taxa"], "Genus2")
        self.assertEqual(result_trees[0]["fia_species_code"], 102)
        self.assertEqual(result_trees[0]["spg"], 0.5)
        self.assertEqual(result_trees[0]["group"], "GroupB")
        self.assertEqual(result_trees[1]["taxa"], "Genus3")
        self.assertEqual(result_trees[1]["fia_species_code"], 103)
        self.assertEqual(result_trees[1]["spg"], 0.7)
        self.assertEqual(result_trees[1]["group"], "GroupC")


if __name__ == "__main__":
    unittest.main()
