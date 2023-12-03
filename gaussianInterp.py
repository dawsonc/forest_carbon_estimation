from abg_biomass import *

import json
import pandas as pd

from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

from itertools import product
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# read the tree data and convert to a data frame
f = open('./100_trees.json')
data = pd.DataFrame(list(json.load(f).values())[0])
f.close()

# compute the biomass at each location
table5_filename = "./table5.csv"
df = load_taxa_agb_model_data(table5_filename)
avg_B0 = np.mean(df.B0) ## use the average values as a substitute
avg_B1 = np.mean(df.B1)
bm = []

for index, row in data.iterrows():
  #b0, b1, r2, dclass = abg_biomass_model(group, taxa, spg, df)
  #print(abg_biomass_model(group, taxa, spg, df))
  #biomass(b0, b1, dclass,dbhvalue)
  bm.append(biomass(avg_B0, avg_B1, "dbh", dbhvalue=row[0]*100))  ## dbh appears to be in meter, so convert to cm

data['biomass'] = bm

# spatial interpolation using Gaussian process
kernel = C(50.0) * RBF([50,50])
gp = GPR(normalize_y=True, alpha=0.3, kernel=kernel)

gp.fit(data[['x_pos', 'y_pos']].values, data.biomass)

# predict at grid points
x_pos_new = np.linspace(data.x_pos.min(), data.x_pos.max()) #p
y_pos_new = np.linspace(data.y_pos.min(), data.y_pos.max()) #q
pos_new = np.array(list(product(x_pos_new, y_pos_new)))
bm_pred, MSE = gp.predict(pos_new, return_std=True)
X0p, X1p = pos_new[:,0].reshape(50,50), pos_new[:,1].reshape(50,50)
Zp = np.reshape(bm_pred,(50,50))

# plot
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.pcolormesh(X0p, X1p, Zp)

plt.show()