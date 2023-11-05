import unittest

from forest_carbon import single_tree_estimation

# The class you're testing
# class YourClass:
#     def add(self, a, b):
#         return a + b


# Test class that inherits from unittest.TestCase
class TestSingleTreeEstimation(unittest.TestCase):
    # Test methods start with the word "test"
    def test_pantropical_tree_model(self):
        agb_func = single_tree_estimation.create_AGB_function(0.0673, 0.926)
        agb = single_tree_estimation.apply_AGB_model(agb_func, 1, 2, 3)
        self.assertEqual(round(agb, 3), 0.672)  # Assert that result is equal to 5


if __name__ == "__main__":
    unittest.main()
