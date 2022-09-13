# ======================================================================================================================
# Name:                 Hamiltonian Construction Module 'hamiltonian.py'
# Description:          1.This module contains functions for constructing custom Hamiltonian.
#                       2. There are prebuilt hamiltonian in 'Netket_module.operator' library. Check following link.
#                       3. Prebuilt Hamiltonian can be used directly in main simulation module.
# Library Dependencies: 1. Netket_module.operator ("https://netket.readthedocs.io/en/latest/api/operator.html")
#                       3. os ("https://docs.python.org/3/library/os.html")
# Author:               Avishek Singh
# Date:                 18.05.2022
# Latest Update:        19.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
from netket import operator
from netket.operator import Ising, Heisenberg
import os
# ======================================================================================================================

# ====== Defining Hamiltonian Functions ================================================================================
# ------ Defining prebuilt Hamiltonian -----------------------------------------------------------------------------
def hamiltonian(hilbert, graph, J, h) -> operator:
    # This Hamiltonian is used for heisenberg model in external magnetic field.
    from netket.operator.spin import sigmaz
    ha = (-J/4) * sum([sigmaz(hilbert, i) * sigmaz(hilbert, j) for (i, j) in graph.edges()])
    ha += (-h/2) * sum([sigmaz(hilbert, i) for i in graph.nodes()])
    return ha
# ----------------------------------------------------------------------------------------------------------------------

# ------ Defining a function to write or print the lattice information to a file ("hamiltonian_info.txt") --------------
def hamiltonian_info(ha: operator) -> None:
    from parameters import print_hamiltonian_info, write_hamiltonian_info
    if print_hamiltonian_info:
        # Print hamiltonian information
        print(f"Hamiltonian is acting on: {ha.acting_on}")
        print(f"Hamiltonian is hermitian: {ha.is_hermitian}")
        print(f"Total hamiltonian operators: {ha.n_operators}")
        print(f"List of operators: {ha.operators}")
    if write_hamiltonian_info:
        from parameters import path_to_hamiltonian_info as path
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        writePath = os.path.join(path, "hamiltonian_info.txt")
        # Writing hamiltonian info to file
        with open(writePath, "w") as hamiltonian_info_file:
            hamiltonian_info_file.write(f"Hamiltonian is acting on: {ha.acting_on}\n")
            hamiltonian_info_file.write(f"Hamiltonian is hermitian: {ha.is_hermitian}\n")
            hamiltonian_info_file.write(f"Total hamiltonian operators: {ha.n_operators}\n")
            hamiltonian_info_file.write(f"List of operators: {ha.operators}\n")
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
