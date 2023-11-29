"""
Kriging model to predict DBH of trees. Testing out how the model works. Based off of
code from https://github.com/GeostatsGuy/PythonNumericalDemos/blob/master/GeostatsPy_kriging.ipynb
"""
from pykrige.ok import OrdinaryKriging
import numpy as np  # arrays and matrix math
from numpy import genfromtxt
import pandas as pd  # DataFrames
import matplotlib.pyplot as plt  # plotting

fraction_data = 1.0

data = genfromtxt('../data/1000_trees_spatial_copy.csv', delimiter=',')
print(data)

# df = pd.read_csv("../data/1000_trees_spatial.csv")

# df["x_pos"] = df["x_pos"].astype(np.float64)
# df["y_pos"] = df["y_pos"].astype(np.float64)
# df["dbh"] = df["dbh"].astype(np.float64)

# if fraction_data < 1.0:
#     df = df.sample(frac=fraction_data, replace=False, random_state=73073)
# df = df.reset_index()
# df = df.iloc[:, 1:]  # excludes first columns, which is the index.
# print(df.head())

# print(df.describe().transpose())

OK = OrdinaryKriging(
    data[:, 0],
    data[:, 2],
    data[:, 3],
    variogram_model="linear",
    verbose=True,
    enable_plotting=False,
)
gridx = np.arange(0.0, 13.0, 1.0)
gridy = np.arange(0.0, 13.0, 1.0)
z, ss = OK.execute("grid", gridx, gridy)
plt.imshow(z)
plt.show()
