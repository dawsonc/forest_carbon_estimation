"""
Kriging model to predict DBH of trees. Testing out how the model works. Based off of
code from https://github.com/GeostatsGuy/PythonNumericalDemos/blob/master/GeostatsPy_kriging.ipynb
"""
import geostatspy.GSLIB as GSLIB                        # GSLIB utilities, visualization and wrapper
import geostatspy.geostats as geostats                  # GSLIB methods convert to Python 
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
import os                                               # to set current working directory 
import numpy as np                                      # arrays and matrix math
import pandas as pd                                     # DataFrames
import matplotlib.pyplot as plt                         # plotting

fraction_data = 1.0

df = pd.read_csv("../data/1000_trees_spatial.csv")

df['x_pos'] = df['x_pos'].astype(np.float64)
df['y_pos'] = df['y_pos'].astype(np.float64)
df['dbh'] = df['dbh'].astype(np.float64)

if fraction_data < 1.0:
    df = df.sample(frac=fraction_data, replace=False, random_state=73073)
df = df.reset_index()
# df = df.iloc[:, 1:]  # excludes first columns, which is the index.
print(df.head())

print(df.describe().transpose())

OK = OrdinaryKriging(df['x_pos'], df['y_pos'], df['dbh'], variogram_model = "linear", verbose = True, enable_plotting = False)
gridx = np.arange(0, 13, 1)
gridy = np.arange(0, 13, 1)
z, ss = OK.execute("grid", gridx, gridy)
plt.imshow(z)
plt.show()
