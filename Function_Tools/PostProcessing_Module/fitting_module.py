# ======================================================================================================================
# Name:                  Data Fitting Module 'fitting_module.py'
# Description:           This module contains functions to post process the results of the simulation.
# Library Dependencies:  1. numpy ("https://numpy.org/")
#                        2. os ("https://docs.python.org/3/library/os.html")
#                        3. pandas ("https://pandas.pydata.org/")
# Author:                Avishek Singh
# Date:                  29.05.2022
# Latest Update:         30.05.2022
# Version:               1.0.0
# ======================================================================================================================

# ====== Importing Required Libraries ==================================================================================
import numpy as np
import pandas as pd
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import inspect
# ======================================================================================================================

# ====== Data Fitting Module ===========================================================================================
# ------ Function to fit magnetization data ----------------------------------------------------------------------------
def fit_mag(function, input_datafile, out_file, show_plot=False, save_plot=False):
    if os.path.exists(input_datafile):
        df = pd.read_fwf(input_datafile)
        df_fit = pd.DataFrame()
        args = inspect.getfullargspec(function).args
        for col in df.columns:
            if col == '#h':
                df_fit[args[0]] = args[1:]
            if col != '#h':
                param, param_cov = curve_fit(function, df['#h'], df[col])
                df_fit[col] = param
                ans = function(df['#h'], *param)
                plt.plot(df['#h'], ans, 'r-', label='Fitted curve', linewidth=3)
                plt.plot(df['#h'], df[col], 'bo', label='Magnetization Data')
                plt.xlabel('h')
                plt.ylabel('MSZ')
                plt.title('Magnetization Data Fitting '+col)
                plt.legend()
                if show_plot is True:
                    plt.show()
                if save_plot is True:
                    from parameters import fitted_plot_path, source_path
                    plot_path = os.path.join(source_path, fitted_plot_path)
                    if not os.path.exists(plot_path):
                        os.makedirs(plot_path)
                    plot_file = plot_path + out_file + '_plot_' + '(' + col + ').pdf'
                    plt.savefig(plot_file, format='pdf')
                plt.close()
        from parameters import source_path, fitting_param_path
        param_path = os.path.join(source_path, fitting_param_path)
        if not os.path.exists(param_path):
            os.makedirs(param_path)
        param_file = param_path + out_file + '_param.txt'
        with open(param_file, 'w') as file:
            dfAsString = df_fit.to_string(header=True, index=False)
            file.write(dfAsString)
    else:
        raise FileNotFoundError('File not found')
# ----------------------------------------------------------------------------------------------------------------------
from parameters import source_path, J_parsed_file_path
def func(x, a, b, c, d):
    return a * np.tanh(b * x - c) + d
path = source_path + J_parsed_file_path + 'PerSite_MSZ.txt'
fit_mag(function=func, input_datafile=path, out_file='MSZ_fit', save_plot=True, show_plot=False)
# ======================================================================================================================
