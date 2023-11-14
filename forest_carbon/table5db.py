import csv
import pandas as pd
import numpy as np

datab = pd.read_csv('table5.csv')
df = pd.DataFrame(datab)
num_rows, num_columns = df.shape

# Adding specific gravity LowerBound & UpperBound Columns to the dataframe

spgLowerBound_str = []
spgUpperBound_str = []

for i in range(num_rows):
   if "/" in df.iloc[i][1]:
      taxaList = df.iloc[i][1].split("/")       
   else:
      taxaList = df.iloc[i][1].split(" ")        # the Taxa column is split to distinguish each element in the column
      
   if "<" in taxaList:
      spgLowerBound_str.append(0.0)
      spgUpperBound_str.append(taxaList[-2])     # e.g. Tsuga < 0.40: taxaList[-2] = 0.40, 0.40 is the upper bound 
   elif ">=" in taxaList:
      spgLowerBound_str.append(taxaList[-2])     
      spgUpperBound_str.append(1.5)              # e.g. Tsuga >= 0.40: taxaList[-2] = 0.40, 0.40 is the lower bound, 1.5 is the set ceiling 
   elif "-" in df.iloc[i][1]:
      boundsDashed = taxaList[-2].split("-")     # e.g. Betulaceae 0.40-0.49
      spgLowerBound_str.append(boundsDashed[0])  # boundsDashed[0] = 0.40, lower bound
      spgUpperBound_str.append(boundsDashed[1])  # boundsDashed[1] = 0.49, upper bound
   elif "spg" not in df.iloc[i][1]:
      spgLowerBound_str.append(0.0)              # range covers all possible spg values
      spgUpperBound_str.append(1.5)              

spgLowerBound = []
spgUpperBound = []

for i in range(0,len(spgLowerBound_str)):        # constructing specific gravity upper and lower bound lists such that each element is a float, not string
   spgLowerBound.append(float(spgLowerBound_str[i]))    
   spgUpperBound.append(float(spgUpperBound_str[i]))

df.insert(10, "Specific Gravity Lower Bound", spgLowerBound)
df.insert(11, "Specific Gravity Upper Bound", spgUpperBound)

  
def abg_biomass_model(group, taxa, spg, dbhvalue):
   """ takes in the group name (str), taxa name (str), and specific gravity (float), and dbh (float)
    returns b0, b1, R^2 statistic, and aboveground biomass for the corresponding model 
    if the user does not supply a specific gravity: 
   returns a list of parameters for all specific gravity ranges for that group/taxa """
 
   matches = 0                                           # initialization of a variable to check if the user input matches a group and taxa column
   parameters = []                                       # initialization of list of parameters if spg is not supplied

   for i in range(num_rows):
      taxaCol = df.iloc[i][1]
      if "/" in df.iloc[i][1]:                           # e.g. ' Fabaceae / Juglandaceae,Carya ' --> ['Fabaceae','Juglandaceae,Carya']
         taxaCol = df.iloc[i][1].split("/")
         for i in range(0,len(taxaCol)):
            taxaCol[i] = taxaCol[i].strip()  

      if df.iloc[i][0] == group and taxa in taxaCol:     # group/taxa name matches user input
         matches += 1
         if spg == None:
            parameters.append((df.iloc[i][10],df.iloc[i][11]))
         else:
            if df.iloc[i][10] <= spg < df.iloc[i][11]:    # spg is in between the upper/lower bound of the group/taxa tree
               b0 = df.iloc[i][3]
               b1 = df.iloc[i][4]
               Rsquared = df.iloc[i][9] 
   
               if df.iloc[i][7] == 'drc':
                  diameter = np.exp(0.36738 + 0.94932 * np.log(dbhvalue))    #converts dbh (input) to drc 
               else:
                  diameter = dbhvalue
               abgBiomass = np.exp(b0 + b1 * np.log(diameter))

   if matches == 0:  #tree is not in the database or the user inupt is incorrect
      return None
   else:
      if spg == None:
         return parameters
      else:
         return b0, b1, Rsquared, abgBiomass
      

# Test Cases
# group = 'Conifer'
# taxa = 'Cupressoceae'
# spg = 0.20
# dbhvalue = 1
# print(abg_biomass_model(group, taxa, spg, dbhvalue))
