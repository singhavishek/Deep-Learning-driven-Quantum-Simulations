# ======================================================================================================================
# Name:                 Hilbert Space Construction Module
# Description:          This module contains functions for constructing Hilbert spaces.
# Library Dependencies: 1. Netket_module.hilbert ("https://netket.readthedocs.io/en/latest/docs/hilbert.html")
#                       2. os ("https://docs.python.org/3/library/os.html")
# Author:               Avishek Singh
# Date:                 18.05.2022
# Latest Update:        18.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
from netket.hilbert import Spin, Fock
import os
# ======================================================================================================================

# ====== Defining Hilbert Space Functions ==============================================================================
# ------ Defining a function to construct Hilbert Space ----------------------------------------------------------------
def hilbert_space(graph) -> object:
    from parameters import hilbert_space_type
    if hilbert_space_type == "spin":
        from parameters import s, total_sz
        if total_sz is None:
            return Spin(s=s, N=graph.n_nodes)
        elif total_sz is not None:
            return Spin(s=s, N=graph.n_nodes, total_sz=total_sz)
        else:
            raise ValueError("Undefined total_sz value.")
    elif hilbert_space_type == "fock":
        from parameters import n_max, N, n_particles
        if n_particles is not None and n_max is not None:
            return Fock(n_max=n_max, n_particles=n_particles, N=N)
        elif n_particles is None and n_max is not None:
            return Fock(n_max=n_max, N=N)
        elif n_particles is not None and n_max is None:
            return Fock(n_particles=n_particles, N=N)
        elif n_particles is None and n_max is None:
            return Fock(N=N)
        else:
            raise ValueError("Undefined n_max and n_particles values.")
    else:
        raise ValueError("Undefined hilbert_space_type value.")
# ======================================================================================================================
# ----------------------------------------------------------------------------------------------------------------------

# ------ Defining a function to write or print the Hilbert information to a file ("hilbert_info.txt") ------------------
def hilbert_info(hilbert) -> None:
    from parameters import print_hilbert_info, write_hilbert_info
    if print_hilbert_info:
        # Printing the Hilbert information to the console
        print(f"Is Hilbert Space Constrained: {hilbert.constrained}")
        print(f"Is Hilbert Space Finite: {hilbert.is_finite}")
        print(f"Is Hilbert Space indexable: {hilbert.is_indexable}")
        print(f"Size of local degrees of freedom: {hilbert.local_size}")
        print(f"Total number of degrees of freedom: {hilbert.size}")
        print(f"The total dimension of the many-body Hilbert space: {hilbert.n_states}")
    if write_hilbert_info:
        from parameters import path_to_hilbert_info as path
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        writePath = os.path.join(path, "hilbert_info.txt")
        # Writing the Hilbert information to a file "hilbert_info.txt"
        with open(writePath, "w") as hilbert_info_file:
            hilbert_info_file.write(f"Is Hilbert Space Constrained: {hilbert.constrained}\n")
            hilbert_info_file.write(f"Is Hilbert Space Finite: {hilbert.is_finite}\n")
            hilbert_info_file.write(f"Is Hilbert Space indexable: {hilbert.is_indexable}\n")
            hilbert_info_file.write(f"Size of local degrees of freedom: {hilbert.local_size}\n")
            hilbert_info_file.write(f"Total number of degrees of freedom: {hilbert.size}\n")
            hilbert_info_file.write(f"The total dimension of the many-body Hilbert space: {hilbert.n_states}\n")
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
