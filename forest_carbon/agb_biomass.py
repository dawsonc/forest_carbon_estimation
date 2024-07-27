from typing import Tuple, Union

import numpy as np
import pandas as pd


def load_taxa_agb_model_data(filename: str) -> pd.DataFrame:
    """
    Reads the contents of a file, with data given as a csv file. Processes the data by creating a dataframe
    that has two additional columns: the lower and upper bounds of the specific gravity.

    Args:
        filename (str): The name of a data file.

    Returns:
        df (pd.DataFrame): A dataframe of the processed data.
    """
    datab = pd.read_csv(filename)
    df = pd.DataFrame(datab)
    num_rows, num_columns = df.shape

    # processing the dataframe
    spgLowerBound_str = []
    spgUpperBound_str = []
    for i in range(num_rows):
        if "/" in df.iloc[i, 1]:
            taxaList = df.iloc[i, 1].split("/")
        else:
            taxaList = df.iloc[i, 1].split(
                " "
            )  # the Taxa column is split to distinguish each element in the column
        if "<" in taxaList:
            spgLowerBound_str.append(0.0)
            spgUpperBound_str.append(
                taxaList[-2]
            )  # e.g. Tsuga < 0.40: taxaList[-2] = 0.40, 0.40 is the upper bound
        elif ">=" in taxaList:
            spgLowerBound_str.append(taxaList[-2])
            spgUpperBound_str.append(
                1.5
            )  # e.g. Tsuga >= 0.40: taxaList[-2] = 0.40, 0.40 is the lower bound, 1.5 is the set ceiling
        elif "-" in df.iloc[i, 1]:
            boundsDashed = taxaList[-2].split("-")  # e.g. Betulaceae 0.40-0.49
            spgLowerBound_str.append(
                boundsDashed[0]
            )  # boundsDashed[0] = 0.40, lower bound
            spgUpperBound_str.append(
                boundsDashed[1]
            )  # boundsDashed[1] = 0.49, upper bound
        elif "spg" not in df.iloc[i, 1]:
            spgLowerBound_str.append(0.0)  # range covers all possible spg values
            spgUpperBound_str.append(1.5)

    spgLowerBound = []
    spgUpperBound = []
    for i in range(
        0, len(spgLowerBound_str)
    ):  # constructing specific gravity upper and lower bound lists such that each element is a float, not string
        spgLowerBound.append(float(spgLowerBound_str[i]))
        spgUpperBound.append(float(spgUpperBound_str[i]))

    df.insert(10, "Specific Gravity Lower Bound", spgLowerBound)
    df.insert(11, "Specific Gravity Upper Bound", spgUpperBound)
    return df


def agb_biomass_model(
    group: str, taxa: str, spg: float, df: pd.DataFrame
) -> Union[
    dict[Tuple[str, str], Tuple[float, float, float, str]],
    Tuple[float, float, float, str],
]:
    """
    Finds the corresponding linear regression model and "class" of the diameter of a tree
    by its group, taxa, and specific gravity, which is passed into the function by the user.
    If the user does not supply a specific gravity, returns a dict
    where the keys are the group and taxa of the tree and the values are a tuple of parameters
    for all specific gravity ranges for that group/taxa.

    Args:
       group (str) - The group of the tree
       taxa (str) - The taxa of the tree
       spg (float) - The specific gravity of the tree
       df - the dataframe called by the function load_taxa_agb_model_data


     Returns:
         b0 (float) - linear regression parameter for the corresponding model
         b1 (float) - linear regression parameter for the corresponding model
         R^2 (float) - linear regression parameter (error) for the corresponding model
         diameterClass (str) - the "class" of the diameter for the corresponding model, either dbh or drc

         If multiple matches are found, return a dictionary of such tuples.
    """
    num_rows, num_columns = df.shape

    matches = 0
    exact_match = False  # initialization of a variable to check if the user input matches a group and taxa column
    parameters = {}  # initialization of list of parameters if spg is not supplied

    for i in range(num_rows):
        taxaCol = df.iloc[i, 1]
        if (
            "/" in df.iloc[i, 1]
        ):  # e.g. ' Fabaceae / Juglandaceae,Carya ' --> ['Fabaceae','Juglandaceae,Carya']
            taxaCol = df.iloc[i, 1].split("/")
            for j in range(0, len(taxaCol)):
                taxaCol[j] = taxaCol[j].strip()

        if (
            df.iloc[i, 0] == group and taxa in taxaCol
        ):  # group/taxa name matches user input
            parameters[(df.iloc[i, 0], df.iloc[i, 1])] = (
                df.iloc[i, 3],
                df.iloc[i, 4],
                df.iloc[i, 9],
                df.iloc[i, 7],
            )
            matches += 1
            if spg is not None:
                if (
                    df.iloc[i, 10] <= spg < df.iloc[i, 11]
                ):  # spg is in between the upper/lower bound of the group/taxa tree
                    exact_match = True  # should not have more than one exact match
                    b0 = float(df.iloc[i, 3])
                    b1 = float(df.iloc[i, 4])
                    Rsquared = float(df.iloc[i, 9])
                    diameterClass = df.iloc[i, 7]  # "drc" or "dbh"
    if matches == 0:  # tree is not in the database or the user inupt is incorrect
        print("Check inputs, no matches found")
    elif exact_match:
        return b0, b1, Rsquared, diameterClass

    return parameters


def biomass(b0: float, b1: float, diameterClass: str, dbhvalue: float) -> float:
    """
    Estimates the aboveground biomass of a tree using linear regression parameters, the "class" of the diameter,
    and the dbh value.

     Args:
         b0 (float) - linear regression parameter for the corresponding model
         b1 (float) - linear regression parameter for the corresponding model
         diameterClass (str) - the "class" of the diameter for the corresponding model, either dbh or drc
         dbhvalue (float) - the value for the dbh of the tree.

     Returns:
         agbBiomass (float) - the estimated aboveground biomass of the tree

     Raises:
         ValueError
    """
    if diameterClass == "drc":
        diameter = np.exp(
            0.36738 + 0.94932 * np.log(dbhvalue)
        )  # converts dbh (input) to drc
    elif diameterClass == "dbh":
        diameter = dbhvalue
    else:
        raise ValueError
    agbBiomass = np.exp(b0 + b1 * np.log(diameter))
    return agbBiomass
