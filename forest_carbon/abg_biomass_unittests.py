import unittest

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

if __name__ == "__main__":
    unittest.main()
    unittest.main()
