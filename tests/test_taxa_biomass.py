import os
import unittest

from forest_carbon import agb_biomass

# Get the file path relative to the current file.
# This file is in the tests directory, so we need to go up one level to get to the data directory.
table5_filename = os.path.join(
    os.path.dirname(__file__),
    "..",
    "forest_carbon",
    "data",
    "taxa_level_agb_model_parameters.csv",
)


class Test_agbBiomass(unittest.TestCase):
    def test_agbBiomass_model_1(self):
        group = "Conifer"
        taxa = "Cupressoceae"
        spg = 0.20
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        model_para = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, (-1.9615, 2.1063, 0.76, "dbh"))

    def test_agbBiomass_model_2(self):
        group = "Conifer"
        taxa = "Cupressoceae"
        spg = 0.40
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        model_para = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, (-2.6327, 2.4757, 0.76, "dbh"))

    def test_agbBiomass_model_3(self):
        group = "Conifer"
        taxa = "Cupressoceae"
        spg = None
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        model_para = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(
            model_para,
            {
                ("Conifer", "Cupressoceae < 0.30 spg"): (-1.9615, 2.1063, 0.76, "dbh"),
                ("Conifer", "Cupressoceae 0.30-0.39 spg"): (
                    -2.7765,
                    2.4195,
                    0.76,
                    "dbh",
                ),
                ("Conifer", "Cupressoceae >= 0.40 spg"): (-2.6327, 2.4757, 0.76, "dbh"),
            },
        )

    def test_agbBiomass_model_4(self):
        group = "Woodland"
        taxa = "Fabaceae"
        spg = 0.5
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        model_para = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(model_para, (-2.9255, 2.4109, 0.89, "drc"))

    def test_agbBiomass_model_5(self):
        group = "Hardwood"
        taxa = "Fabaceae"
        spg = None
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        model_para = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(
            model_para,
            {
                ("Hardwood", "Fabaceae / Juglondoceoe,Carya"): (
                    -2.5095,
                    2.6175,
                    0.81,
                    "dbh",
                ),
                ("Hardwood", "Fabaceae / Juglondoceoe,other"): (
                    -2.5095,
                    2.5437,
                    0.81,
                    "dbh",
                ),
            },
        )

    def test_agbBiomass_model_6(self):
        group = "Hardwood"
        taxa = "Fagaceae evergreen"
        spg = None
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        model_para = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(
            model_para,
            {("Hardwood", "Fagaceae evergreen"): (-2.2198, 2.441, 0.84, "dbh")},
        )

    def test_agbBiomass(self):
        group = "Woodland"
        taxa = "Cupressoceae"
        spg = 0.7
        dbhvalue = 1
        df = agb_biomass.load_taxa_agb_model_data(table5_filename)
        b0, b1, r2, dclass = agb_biomass.agb_biomass_model(group, taxa, spg, df)
        self.assertEqual(round(agb_biomass.biomass(b0, b1, dclass, dbhvalue), 2), 0.15)


if __name__ == "__main__":
    unittest.main()
    unittest.main()
