# ======================================================================================================================
# Name:                  Graph Plotting Module 'graph_module.py'
# Description:           This module contains functions to plot graphs.
# Library Dependencies:  1. Matplotlib ('https://matplotlib.org/')
# Author:                Avishek Singh
# Date:                  25.05.2022
# Latest Update:         25.05.2022
# Version:               1.0.0
# ======================================================================================================================

# ====== Importing Required Libraries ==================================================================================
import matplotlib.pyplot as plt
import os
import pandas as pd
# ======================================================================================================================

# ====== Functions to Plot Graphs ======================================================================================
# ------ Basic Graph Plotting Function ---------------------------------------------------------------------------------
def basic_plot(x, y, x_label, y_label, title):
    """
    This function plots a basic graph.
    :param show_plot: To show the plot or not.
    :param x: x-axis data
    :param y: y-axis data
    :param x_label: x-axis label
    :param y_label: y-axis label
    :param title: graph title
    :param save_path: save path
    :param save_name: save name
    :return: None
    """
    # Plotting the graph
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    return plt
# ----------------------------------------------------------------------------------------------------------------------

# ------ Parsed Data Plotting Function ---------------------------------------------------------------------------------
def parsed_data_plot(parsed_data, show_plot=False, save_plot=True, var1=None, var2=None):
    from parameters import parsed_data_plot_path
    if not os.path.exists(parsed_data_plot_path):
        os.makedirs(parsed_data_plot_path)
    x = parsed_data['iters']
    for key, value in parsed_data.items():
        if key != 'iters':
            plot = basic_plot(x=x, y=value, x_label='Iterations', y_label=key, title=key + ' Vs Iterations')
            if save_plot is True:
                if var1 is not None and var2 is not None:
                    filename = key + '(J=' + str(var1) + ', h=' + str(var2) + ').pdf'
                elif var1 is not None and var2 is None:
                    filename = key + '(J=' + str(var1) + ').pdf'
                elif var1 is None and var2 is not None:
                    filename = key + '(h=' + str(var2) + ').pdf'
                else:
                    filename = key + '.pdf'
                plotPath = os.path.join(parsed_data_plot_path, filename)
                plot.savefig(plotPath, format='pdf')
            if show_plot is True:
                plot.show()
            plot.close()
    return None
# ----------------------------------------------------------------------------------------------------------------------

# ------ J based parsed data plot function -----------------------------------------------------------------------------
def plot_J_based_parsed_data(input_file_path, out_file_path, show_plot=False, save_plot=True):
    if not os.path.exists(out_file_path):
        os.makedirs(out_file_path)
    if os.path.exists(input_file_path):
        for file in os.listdir(input_file_path):
            if file.endswith('.txt'):
                filename = file.split('.')[0]
                df = pd.read_fwf(os.path.join(input_file_path, file))
                data_dict = {}
                for cols in df.columns:
                    if cols == '#h':
                        data_dict[cols] = df[cols].values
                    if cols != '#h':
                        data_dict[cols] = df[cols].values
                        title = filename + '_(' + cols + ')' + ' Vs h'
                        y_label = filename
                        plot = basic_plot(x=df['#h'], y=df[cols], x_label='h', y_label=y_label, title=title)
                        if save_plot is True:
                            plotPath = os.path.join(out_file_path, filename + '_(' + cols + ').pdf')
                            plot.savefig(plotPath, format='pdf')
                        if show_plot is True:
                            plot.show()
                        plot.close()
                for key, value in data_dict.items():
                    if key != '#h':
                        plt.plot(data_dict['#h'], data_dict[key], label=key)
                        plt.xlabel('h')
                        plt.ylabel(filename)
                        plt.legend()
                if save_plot is True:
                    plotPath = os.path.join(out_file_path, filename + '.pdf')
                    plt.savefig(plotPath, format='pdf')
                if show_plot is True:
                    plt.show()
                plt.close()
    else:
        raise FileNotFoundError('Input file path does not exist')
    return None
# ----------------------------------------------------------------------------------------------------------------------
from parameters import source_path, J_parsed_file_path, path_plots, J_parsed_plot_path
inp_path = os.path.join(source_path, J_parsed_file_path)
out_path = os.path.join(source_path, J_parsed_plot_path)
plot_J_based_parsed_data(input_file_path=inp_path, out_file_path=out_path, show_plot=False, save_plot=True)
# ======================================================================================================================
