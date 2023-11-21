import shutil
import unittest
import tempfile
import json
from unittest.mock import patch

from combined_agb_calculator import *
from abg_biomass import *
table5_filename = "./table5.csv"

class Test_abgBiomass(unittest.TestCase):
    def test_abgBiomass_model_1(self):
        group='Conifer'
        taxa = 'Cupressoceae'
        spg = 0.20
        df = load_taxa_agb_model_data(table5_filename)
        model_para = abg_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, (-1.9615, 2.1063, 0.76, 'dbh'))  

    def test_abgBiomass_model_2(self):
        group='Conifer'
        taxa = 'Cupressoceae'
        spg = 0.40
        df = load_taxa_agb_model_data(table5_filename)
        dbhvalue = 1
        model_para = abg_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, (-2.6327, 2.4757, 0.76, 'dbh'))

    def test_abgBiomass_model_3(self):
        group='Conifer'
        taxa = 'Cupressoceae'
        spg = None
        dbhvalue = 1
        df = load_taxa_agb_model_data(table5_filename)
        model_para = abg_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, [(-1.9615, 2.1063, 0.76, 'dbh'), (-2.7765, 2.4195, 0.76, 'dbh'), 
                                      (-2.6327, 2.4757, 0.76, 'dbh')])
        
    def test_abgBiomass_model_3(self):
        group='Woodland'
        taxa = 'Fabaceae'
        spg = 0.5
        df = load_taxa_agb_model_data(table5_filename)
        model_para = abg_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, (-2.9255, 2.4109, 0.89, 'drc'))

    def test_abgBiomass_model_4(self):
        group='Hardwood'
        taxa = 'Fabaceae'
        spg = 0.5
        df = load_taxa_agb_model_data(table5_filename)
        model_para = abg_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, [(-2.5095, 2.6175, 0.81, 'dbh'), (-2.5095, 2.5437, 0.81, 'dbh')])

    def test_abgBiomass(self):
        group='Woodland'
        taxa = 'Cupressoceae2'
        spg = 0.7
        dbhvalue = 1
        df = load_taxa_agb_model_data(table5_filename)
        b0, b1, r2, dclass = abg_biomass_model(group, taxa, spg, df)
        self.assertEqual(round(biomass(b0, b1, dclass,dbhvalue), 2), 0.15)



class TestYourModule(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    def test_load_tree_data_from_json(self):
        test_json = os.path.join(self.test_dir, 'test_data.json')
        with open(test_json, 'w') as f:
            json.dump({"trees": [{"dbh": 10, "species": "Oaks", "x_pos": 1, "y_pos": 2}]}, f)
        result = load_tree_data_from_json(test_json, "path/to/species_info.csv")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['dbh'], 10)

    def test_choosing_the_model(self):
        with patch('abg_biomass.abg_biomass_model', return_value=[1, 2, 3, 4]):
            with patch('abg_biomass.biomass', return_value=42):
                with patch('single_tree_estimation.apply_AGB_model', return_value=24):
                    with patch('single_tree_estimation.apply_AGB_model_no_height', return_value=18):
                        result = choosing_the_model("Group1", "Taxa1", 10, 0.5, 5, None, None, None)
        self.assertEqual(result, 42)

    def test_apply_model(self):
        with patch('your_module.choosing_the_model', return_value=42):
            test_data = [{"group": "Group1", "taxa": "Taxa1", "dbh": 10, "spg": 0.5, "height": 5}]
            result = apply_model(test_data, "path/to/taxa_level_parameters.csv")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get('ABG value'), 42)

    def test_run_model(self):
        with patch('your_module.load_tree_data_from_json', return_value=[{"species": "Oaks", "dbh": 10, "x_pos": 1, "y_pos": 2}]):
            with patch('your_module.apply_model', return_value=[{"species": "Oaks", "dbh": 10, "x_pos": 1, "y_pos": 2, "ABG value": 42}]):
                run_model(self.test_dir, self.test_dir, self.test_dir)

if __name__ == "__main__":
    unittest.main()
    unittest.main()
