# ======================================================================================================================
# Name:                 Observable (Properties) Module 'observables.py'
# Description:          This module contains functions for to define observables to compute properties while simulation.
# Library Dependencies: 1. Netket_module.graph ("https://netket.readthedocs.io/en/latest/api/graph.html")
#                       2. os ("https://docs.python.org/3/library/os.html")
# Author:               Avishek Singh
# Date:                 20.05.2022
# Latest Update:        26.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
from netket.operator import LocalOperator
from netket.operator.spin import sigmaz, sigmax, sigmay
# ======================================================================================================================

# ====== Defining Observable Functions =================================================================================
obs_list = ['MSX', 'MSY', 'MSZ', 'chi_corrZ']
# ======================================================================================================================
# ------ Defining Observable list --------------------------------------------------------------------------------------
def observables(hilbert, graph, J):
    obs_dict = {}
    for items in obs_list:
        if items == 'MSX':
            obs_dict[items] = LocalOperator(hilbert, dtype=complex)
            obs_dict[items] = sum([sigmax(hilbert, i) / 2 for i in graph.nodes()])
        elif items == 'MSY':
            obs_dict[items] = LocalOperator(hilbert, dtype=complex)
            obs_dict[items] = sum([sigmay(hilbert, i) / 2 for i in graph.nodes()])
        elif items == 'MSZ':
            obs_dict[items] = LocalOperator(hilbert, dtype=complex)
            obs_dict[items] = sum([sigmaz(hilbert, i) / 2 for i in graph.nodes()])
        elif items == 'chi_corrZ':
            obs_dict[items] = LocalOperator(hilbert, dtype=complex)
            obs_dict[items] = sum([-J * sigmay(hilbert, i) * sigmay(hilbert, j) for i, j in graph.edges()])
        else:
            raise ValueError('Observables not defined')
    if obs_list != list(obs_dict.keys()):
        raise ValueError(f'Observables not defined')
    else:
        return obs_dict
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
