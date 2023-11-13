"""
Kriging model to predict DBH of trees. Testing out how the model works. Based off of
code from https://github.com/GeostatsGuy/PythonNumericalDemos/blob/master/GeostatsPy_kriging.ipynb
"""

import pandas as pd  # DataFrames

fraction_data = 1.0

df = pd.read_csv("../data/100_trees.csv")

if fraction_data < 1.0:
    df = df.sample(frac=fraction_data, replace=False, random_state=73073)
df = df.reset_index()
df = df.iloc[:, 1:]  # excludes first columns, which is the index.
print(df.head())

print(df.describe().transpose())
