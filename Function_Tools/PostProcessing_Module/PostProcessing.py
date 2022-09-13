# ======================================================================================================================
# Name:                  Post Processing Module 'PostProcessing.py'
# Description:           This module contains functions to post process the results of the simulation.
# Library Dependencies:  1. numpy ("https://numpy.org/")
#                        2. os ("https://docs.python.org/3/library/os.html")
#                        3. pandas ("https://pandas.pydata.org/")
# Author:                Avishek Singh
# Date:                  20.05.2022
# Latest Update:         29.05.2022
# Version:               1.0.0
# ======================================================================================================================

# ====== Importing Required Libraries ==================================================================================
import numpy as np
import pandas as pd
import os
from jax import grad
# ======================================================================================================================

# ====== Post Processing Module ========================================================================================
# ------ Per Site Data Processing --------------------------------------------------------------------------------------
def perSiteData(directory_path, column_names):
    from Function_Tools.Netket_module.lattice import lattice
    gp = lattice()
    for file in os.listdir(directory_path):
        if file.endswith(".txt"):
            filePath = directory_path + file
            df = pd.read_fwf(filePath)
            for column in column_names:
                df[column] = df[column]/gp.n_nodes
            writePath = directory_path + "PerSite_" + file
            with open(writePath, 'w') as file_df:
                dfAsString = df.to_string(header=True, index=False)
                file_df.write(dfAsString)
    return None
# ----------------------------------------------------------------------------------------------------------------------

# ------ Compute magnetic susceptibility -------------------------------------------------------------------------------
def computeMagneticSusceptibility_old():
    from parameters import source_path, J_parsed_file_path
    path = os.path.join(source_path, J_parsed_file_path)
    ms_file = os.path.join(path, "PerSite_MSZ.txt")
    if os.path.exists(ms_file):
        ms_df = pd.read_fwf(ms_file)
        chi_df = pd.DataFrame()
        for cols in ms_df.columns:
            if cols == "#h":
                chi_df["#h"] = ms_df["#h"]
            else:
                chi_df[cols] = ms_df[cols]/ms_df["#h"]
        filePath = os.path.join(path, "chi.txt")
        with open(filePath, 'w') as file_df:
            dfAsString = chi_df.to_string(header=True, index=False)
            file_df.write(dfAsString)
    else:
        raise FileNotFoundError("MSZ.txt not found in the specified path")
    return None

def computeMagneticSusceptibility():
    from parameters import source_path, J_parsed_file_path
    ms_file = os.path.join(source_path, J_parsed_file_path, "PerSite_MSZ.txt")
    if os.path.exists(ms_file):
        ms_df = pd.read_fwf(ms_file)
        chi_df = pd.DataFrame()
        for cols in ms_df.columns:
            if cols == "#h":
                chi_df["#h"] = ms_df["#h"][0:len(ms_df["#h"])-1]
                dh = [ms_df[cols].values[i + 1] - ms_df[cols].values[i] for i in range(len(ms_df[cols].values) - 1)]
                chi_df["dh"] = dh
            else:
                dm = np.abs([ms_df[cols].values[i + 1] - ms_df[cols].values[i] for i in range(len(ms_df[cols].values)-1)])
                dh = [ms_df["#h"].values[i + 1] - ms_df["#h"].values[i] for i in range(len(ms_df["#h"].values)-1)]
                chi_df["m-" + cols] = ms_df[cols][0:len(ms_df["#h"]) - 1]
                chi_df['dm-'+cols] = dm
                chi_df['chi-' + cols] = [dm[i]/dh[i] for i in range(len(dm))]
                filePath = os.path.join(source_path, J_parsed_file_path)
                if not os.path.exists(filePath):
                    os.mkdir(filePath)
                filename = os.path.join(filePath, "chi.txt")
                with open(filename, 'w') as file_df:
                    dfAsString = chi_df.to_string(header=True, index=False)
                    file_df.write(dfAsString)
    else:
        raise FileNotFoundError("PerSite_MSZ.txt not found in the specified path")
    return None
# ----------------------------------------------------------------------------------------------------------------------

# ------ Compute angle between two Spins -------------------------------------------------------------------------------
def computeAngle():
    from parameters import source_path, J_parsed_file_path
    path = os.path.join(source_path, J_parsed_file_path)
    ms_file = os.path.join(path, "PerSite_MSZ.txt")
    if os.path.exists(ms_file):
        ms_df = pd.read_fwf(ms_file)
        angle_df = pd.DataFrame()
        for cols in ms_df.columns:
            if cols == "#h":
                angle_df["#h"] = ms_df["#h"]
            else:
                angle_df[cols] = np.arccos(4 * np.abs(ms_df[cols]) - 1)
        filePath = os.path.join(path, "Angle.txt")
        with open(filePath, 'w') as file_df:
            dfAsString = angle_df.to_string(header=True, index=False)
            file_df.write(dfAsString)
    else:
        raise FileNotFoundError("MSZ.txt not found in the specified path")
    return None
# ----------------------------------------------------------------------------------------------------------------------
computeMagneticSusceptibility()
# ======================================================================================================================
