# ======================================================================================================================
# Name:                 Main Simulation Module 'main.py'
# Description:          1. This module is designed to run simulation.
#                       2. All the components required to run the simulation are called in this module
#                       3. Modify This file to run simulation with different 'J' & 'h' or loop over different parameters
# Library Dependencies: 1. numpy ("https://numpy.org/")
#                       2. os ("https://docs.python.org/3/library/os.html")
#                       3. tqdm ("https://tqdm.github.io/")
# Author:               Avishek Singh
# Date:                 22.05.2022
# Latest Update:        25.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ========= Importing and setting up the libraries =====================================================================
# ----- Importing OS and setting code to run on CPU or GPU -------------------------------------------------------------
from parameters import run_type

if run_type == "cpu":
    import os

    os.environ["JAX_PLATFORM_NAME"] = "cpu"
elif run_type == "gpu":
    import os

    os.environ["JAX_PLATFORM_NAME"] = "gpu"
else:
    print("Run type not recognised")
    raise ValueError
# ----------------------------------------------------------------------------------------------------------------------

# ----- Importing Numpy ------------------------------------------------------------------------------------------------
import numpy as np
# ----------------------------------------------------------------------------------------------------------------------

# ----- Importing Pandas DataFrame -------------------------------------------------------------------------------------
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------

# ----- Importing Other Libraries --------------------------------------------------------------------------------------
from tqdm import tqdm  # To create progress bar over loops
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

# ======= Main Simulation Module =======================================================================================
if __name__ == "__main__":
    # ========== Running Main Simulation Module ========================================================================
    # ----- Setting up the parameters ----------------------------------------------------------------------------------
    from parameters import J_ex, J_ex_increment, h_ex, h_ex_increment
    h_num = abs(round((min(h_ex) - max(h_ex)) / h_ex_increment)) + 1
    J_num = abs(round((min(J_ex) - max(J_ex)) / J_ex_increment)) + 1
    h_ex_list = np.linspace(min(h_ex), max(h_ex), h_num)
    J_ex_list = np.linspace(min(J_ex), max(J_ex), J_num)
    # ------------------------------------------------------------------------------------------------------------------

    # ----- Loop over different parameters -----------------------------------------------------------------------------
    from HMEX import hmex
    from Function_Tools.Observables.observables import obs_list
    # ------ Creating dataframe list for J, h, and observables ---------------------------------------------------------
    df_jh_list = ['Energy']
    df_jh_list.extend(obs_list)
    df_jh_dict = {}
    for item in df_jh_list:
        df_jh_dict[item] = pd.DataFrame()
    # ------------------------------------------------------------------------------------------------------------------
    for j in (pbar_J := tqdm(J_ex_list, position=0)):
        pbar_J.set_description(f"Running on {run_type} " + "[J = {0:5.2f}]".format(j))
        # ------ Creating dataframe list -------------------------------------------------------------------------------
        df_list = ['Energy']
        df_list.extend(obs_list)
        df_dict = {}
        for item in df_list:
            df_dict[item] = pd.DataFrame()
        dict_mean = {}
        for item in df_list:
            dict_mean[item] = []
        # --------------------------------------------------------------------------------------------------------------
        for h in (pbar_h := tqdm(h_ex_list, position=1, leave=False)):
            pbar_h.set_description(f"Running on {run_type} " + "[h = {0:5.2f}]".format(h))
            # ----- Running the simulation -----------------------------------------------------------------------------
            log, obs_list = hmex(J=j, h=h, show_progress_bar=False)
            # ----------------------------------------------------------------------------------------------------------

            # ----- Parsing data and writing to a file -----------------------------------------------------------------
            from Function_Tools.FileWriting_GraphPloting_Module.File_Module import parse_logger_data

            parsed_data = parse_logger_data(logger_object=log, obs_list=obs_list, write_to_file=True,
                                            j=j, h=h)
            from parameters import n_values
            for key, value in dict_mean.items():
                value.append(np.mean(parsed_data[key][-n_values:]))
            # ----------------------------------------------------------------------------------------------------------

            # ----- Plotting the data ----------------------------------------------------------------------------------
            from Function_Tools.FileWriting_GraphPloting_Module.graph_module import parsed_data_plot
            parsed_data_plot(parsed_data=parsed_data, show_plot=False, save_plot=True, var1=j, var2=h)
            # ----------------------------------------------------------------------------------------------------------

            # ----- Storing Parsed data to a dataframe for all h values ------------------------------------------------
            from Function_Tools.FileWriting_GraphPloting_Module.File_Module import combine_parsed_data
            var_parsed_df = combine_parsed_data(parsed_data=parsed_data, df_dict=df_dict, var=h, var_list=h_ex_list)
            # ----------------------------------------------------------------------------------------------------------

        # ----- Writing J based parsed data to file --------------------------------------------------------------------
        from Function_Tools.FileWriting_GraphPloting_Module.File_Module import write_combined_data_to_file
        write_combined_data_to_file(data_df=var_parsed_df, var=j)
        # --------------------------------------------------------------------------------------------------------------

        # ----- Storing J based parsed data to a dataframe for all J values --------------------------------------------
        for key, df_jh in df_jh_dict.items():
            if j == J_ex_list[0]:
                df_jh['#h'] = h_ex_list
            df_jh['j=' + str(j)] = dict_mean[key]
        # --------------------------------------------------------------------------------------------------------------

    # ----- Writing J based parsed data to file ------------------------------------------------------------------------
    from Function_Tools.FileWriting_GraphPloting_Module.File_Module import write_parsed_data_jh
    write_parsed_data_jh(df_dict=df_jh_dict)
    # ------------------------------------------------------------------------------------------------------------------
    # ==================================================================================================================

    # ====== Post Processing ===========================================================================================
    # ------ Writing persite J & h parsed data -------------------------------------------------------------------------
    from Function_Tools.PostProcessing_Module.PostProcessing import perSiteData
    from parameters import source_path, J_parsed_file_path
    path = os.path.join(source_path, J_parsed_file_path)
    column_list = []
    for items in J_ex_list:
        column_list.append('j=' + str(items))
    perSiteData(path, column_list)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Computing Magnetic Susceptibility -------------------------------------------------------------------------
    from Function_Tools.PostProcessing_Module.PostProcessing import computeMagneticSusceptibility
    computeMagneticSusceptibility()
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Computing angle between spins -----------------------------------------------------------------------------
    from Function_Tools.PostProcessing_Module.PostProcessing import computeAngle
    computeAngle()
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Fit Magnetization -----------------------------------------------------------------------------------------
    from parameters import source_path, J_parsed_file_path
    from Function_Tools.PostProcessing_Module.fitting_module import fit_mag
    def func(x, a, b, c, d):
        return a * np.tanh(b * x - c) + d
    path = source_path + J_parsed_file_path + 'PerSite_MSZ.txt'
    fit_mag(function=func, input_datafile=path, out_file='MSZ_fit', save_plot=True, show_plot=True)
    # ------------------------------------------------------------------------------------------------------------------
    # ==================================================================================================================
# ======================================================================================================================
