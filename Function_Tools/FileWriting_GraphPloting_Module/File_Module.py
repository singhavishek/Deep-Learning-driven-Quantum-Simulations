# ======================================================================================================================
# Name:                  File Handling Module 'File_Module.py'
# Description:           This module contains functions to parse logger data and write it to a file.
# Library Dependencies:  1. Numpy ('https://numpy.org/')
#                        2. Pandas ('https://pandas.pydata.org/docs/index.html')
#                        3. os ('https://docs.python.org/3/library/os.html')
# Author:                Avishek Singh
# Date:                  20.05.2022
# Latest Update:         25.05.2022
# Version:               1.0.0
# ======================================================================================================================

# ====== Importing Required Libraries ==================================================================================
import pandas as pd
import numpy as np
import os
# ======================================================================================================================

# ====== File Handling Module Functions ================================================================================
# ------ Parse Logger Data ---------------------------------------------------------------------------------------------
def parse_logger_data(logger_object, obs_list, write_to_file=False, j=None, h=None):
    data = logger_object.data
    parsed_data_keys = ['iters', 'Energy']
    parsed_data_keys.extend(obs_list)
    parsed_data_df = pd.DataFrame()
    for item in parsed_data_keys:
        if item == 'iters':
            parsed_data_df[item] = np.real(data['Energy'][item])
        else:
            parsed_data_df[item] = np.real(data[item]['Mean'])
    if write_to_file is True:
        from parameters import simulation_file_path
        isExists = os.path.exists(simulation_file_path)
        if not isExists:
            os.makedirs(simulation_file_path)
        if j is not None and h is not None:
            writeFile = 'data_(J=' + str(j) + ',h=' + str(h) + ').txt'
        elif j is None and h is None:
            writeFile = 'data.txt'
        elif j is not None and h is None:
            writeFile = 'data_(J=' + str(j) + ').txt'
        elif j is None and h is not None:
            writeFile = 'data_(h=' + str(h) + ').txt'
        else:
            print('Warning: J and h values not recognized for writing to file. Writing to file as "data.txt".')
            print("If you have loop over J and h values. Please Check the values of J and h.")
            writeFile = 'data.txt'
        writePath = os.path.join(simulation_file_path, writeFile)
        with open(writePath, 'w') as energy_file:
            dfAsString = parsed_data_df.to_string(header=True, index=False)
            energy_file.write(dfAsString)
    return parsed_data_df
# ----------------------------------------------------------------------------------------------------------------------

# ------ Combine Parsed Data -------------------------------------------------------------------------------------------
def combine_parsed_data(parsed_data, df_dict, var, var_list):
    for key, df in df_dict.items():
        if var == var_list[0]:
            df['#iters'] = parsed_data['iters']
        df['h=' + str(var)] = parsed_data[key]
    return df_dict
# ----------------------------------------------------------------------------------------------------------------------

# ------ Write combined variable Data to file --------------------------------------------------------------------------
def write_combined_data_to_file(data_df, var):
    from parameters import var_file_path
    isExists = os.path.exists(var_file_path)
    if not isExists:
        os.makedirs(var_file_path)
    for key, value in data_df.items():
        writeFileName = key + "_(J=" + str(var) + ").txt"
        writePath = os.path.join(var_file_path, writeFileName)
        with open(writePath, 'w') as energy_file:
            dfAsString = value.to_string(header=True, index=False)
            energy_file.write(dfAsString)
    return None
# ----------------------------------------------------------------------------------------------------------------------

# ------ Parse data File For All J and h Values ------------------------------------------------------------------------
def write_parsed_data_jh(df_dict):
    from parameters import J_parsed_file_path
    isExists = os.path.exists(J_parsed_file_path)
    if not isExists:
        os.makedirs(J_parsed_file_path)
    for key, value in df_dict.items():
        filename = key + '.txt'
        writePath = os.path.join(J_parsed_file_path, filename)
        with open(writePath, 'w') as energy_file:
            dfAsString = value.to_string(header=True, index=False)
            energy_file.write(dfAsString)
    return None
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

