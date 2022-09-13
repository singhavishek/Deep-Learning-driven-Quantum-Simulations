# ======================================================================================================================
# Name:                 Observable (Properties) Module 'observables.py'
# Description:          This module contains functions for to define observables to compute properties while simulation.
# Library Dependencies: 1. Netket_module.graph ("https://netket.readthedocs.io/en/latest/api/graph.html")
#                       2. os ("https://docs.python.org/3/library/os.html")
# Author:               Avishek Singh
# Date:                 20.05.2022
# Latest Update:        25.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
from netket.operator import LocalOperator
from netket.operator.spin import sigmaz, sigmax, sigmay
# ======================================================================================================================

# ====== Defining Observable Functions =================================================================================
# ------ Defining a function to create an observable -------------------------------------------------------------------
def observables(hilbert=None, graph=None, return_obs_list=False):
    # ------ Observable Operator to compute total magnetization --------------------------------------------------------
    if hilbert is not None and graph is not None:
        msz = LocalOperator(hilbert=hilbert, dtype=complex)
        msz = sum([sigmaz(hilbert, i)/2 for i in graph.nodes()])
        msx = LocalOperator(hilbert=hilbert, dtype=complex)
        msx = sum([sigmax(hilbert, i)/2 for i in graph.nodes()])
        msy = LocalOperator(hilbert=hilbert, dtype=complex)
        msy = sum([sigmay(hilbert, i)/2 for i in graph.nodes()])
        # ----------------------------------------------------------------------------------------------------------

        # ------ Listing all observables to a dictionary -----------------------------------------------------------
        obs = {
            "MSZ": msz,
            "MSX": msx,
            "MSY": msy
        }
        if return_obs_list is True:
            return obs, list(obs.keys())
        else:
            return obs
    elif hilbert is None and graph is None:
        obs_list = ['MSZ', 'MSX', 'MSY']
        if return_obs_list is True:
            return obs_list
        else:
            raise ValueError("Set return_obs_list to True.")
    else:
        raise ValueError("Please provide a valid hilbert and graph.")
    # ------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
