import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from forest_carbon import combined_agb_calculator

table5_filename = "./table5.csv"


class TestBiomassCalculator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_json = os.path.join(self.test_dir, "test_data.json")
        with open(self.test_json, "w") as f:
            json.dump(
                {"trees": [{"dbh": 10, "species": "Oaks", "x_pos": 1, "y_pos": 2}]}, f
            )

    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    def test_load_tree_data_from_json(self):
        result = combined_agb_calculator.load_tree_data_from_json(
            self.test_json,
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "forest_carbon",
                "data",
                "tree_species_info.csv",
            ),
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["dbh"], 10)

    def test_choosing_the_model(self):
        with patch(
            "forest_carbon.agb_biomass.agb_biomass_model", return_value=(1, 2, 3, 4)
        ):
            with patch("forest_carbon.agb_biomass.biomass", return_value=42.0):
                with patch(
                    "forest_carbon.single_tree_estimation.apply_AGB_model",
                    return_value=24,
                ):
                    with patch(
                        "forest_carbon.single_tree_estimation.apply_AGB_model_no_height",
                        return_value=18,
                    ):
                        result = combined_agb_calculator.choosing_the_model(
                            "Group1", "Taxa1", 10.0, 0.5, 5, None, None, None
                        )
        self.assertEqual(result, 42)

    def test_apply_model(self):
        with patch(
            "forest_carbon.combined_agb_calculator.choosing_the_model", return_value=42
        ):
            test_data = [
                {"group": "Group1", "taxa": "Taxa1", "dbh": 10, "spg": 0.5, "height": 5}
            ]
            result = combined_agb_calculator.apply_model(
                test_data,
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "forest_carbon",
                    "data",
                    "taxa_level_agb_model_parameters.csv",
                ),
            )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get("ABG value"), 42)

    def test_run_model(self):
        with patch(
            "forest_carbon.combined_agb_calculator.load_tree_data_from_json",
            return_value=[{"species": "Oaks", "dbh": 10, "x_pos": 1, "y_pos": 2}],
        ):
            with patch(
                "forest_carbon.combined_agb_calculator.apply_model",
                return_value=[
                    {
                        "species": "Oaks",
                        "dbh": 10,
                        "x_pos": 1,
                        "y_pos": 2,
                        "ABG value": 42,
                    }
                ],
            ):
                combined_agb_calculator.run_model(
                    self.test_json,
                    os.path.join(self.test_dir, "test_data_processed.csv"),
                )


if __name__ == "__main__":
    unittest.main()
