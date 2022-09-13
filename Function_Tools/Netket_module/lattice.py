# ======================================================================================================================
# Name:                 Lattice Construction Module 'lattice.py'
# Description:          This module contains functions for constructing lattices.
# Library Dependencies: 1. Netket_module.graph ("https://netket.readthedocs.io/en/latest/api/graph.html")
#                       2. os ("https://docs.python.org/3/library/os.html")
# Author:               Avishek Singh
# Date:                 17.05.2022
# Latest Update:        18.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
from netket.graph import Graph, Hypercube, Lattice
import os
# ======================================================================================================================

# ====== Defining Lattice Functions ====================================================================================
# ------ Defining a function to create a lattice -----------------------------------------------------------------------
def lattice() -> Graph:
    from parameters import lattice_type
    if lattice_type == 'hypercube':
        from parameters import length, dim, pbc
        graph = Hypercube(length=length, n_dim=dim, pbc=pbc)
        return graph
    elif lattice_type == 'custom':
        from parameters import basis_vectors, atomic_positions, dimensions, pbc, point_group, neighbor_order
        if point_group is None and neighbor_order is None:
            graph = Lattice(basis_vectors=basis_vectors, atoms_coord=atomic_positions, extent=dimensions,
                                     pbc=pbc)
            return graph
        elif point_group is not None and neighbor_order is not None:
            graph = Lattice(basis_vectors=basis_vectors, atoms_coord=atomic_positions, extent=dimensions,
                            pbc=pbc, point_group=point_group, max_neighbor_order=neighbor_order)
            return graph
        elif point_group is not None and neighbor_order is None:
            graph = Lattice(basis_vectors=basis_vectors, atoms_coord=atomic_positions, extent=dimensions,
                            pbc=pbc, point_group=point_group)
            return graph
        elif point_group is None and neighbor_order is not None:
            graph = Lattice(basis_vectors=basis_vectors, atoms_coord=atomic_positions, extent=dimensions,
                                     pbc=pbc, max_neighbor_order=neighbor_order)
            return graph
        else:
            print("Lattice Nor constructed. Please Look for Documentation")
            return None
    else:
        raise ValueError("Lattice type not found")
# ----------------------------------------------------------------------------------------------------------------------

# ------ Defining a function to write or print the lattice information to a file ("lattice_info.txt") ------------------
def lattice_info(graph: Graph) -> None:
    from parameters import print_lattice_info, write_lattice_info
    if print_lattice_info:
        # Print lattice information
        print(f"Is lattice Bipartite: {graph.is_bipartite()}")
        print(f"Total sites in lattice: {graph.n_nodes}")
        print(f"Total edges in lattice: {graph.n_edges}")
        print(f"Total symmetry operations: {len(graph.automorphisms())}")
        print(f"Edges in Lattice: {graph.edges()}")

    if write_lattice_info:
        from parameters import path_to_lattice_info as path
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        writePath = os.path.join(path, "lattice_info.txt")
        # Writing lattice info to file
        with open(writePath, "w") as lattice_info_file:
            lattice_info_file.write(f"Is lattice Bipartite: {graph.is_bipartite()}\n")
            lattice_info_file.write(f"Total sites in lattice: {graph.n_nodes}\n")
            lattice_info_file.write(f"Total edges in lattice: {graph.n_edges}\n")
            lattice_info_file.write(f"Total symmetry operations: {len(graph.automorphisms())}\n")
            lattice_info_file.write(f"Edges in Lattice: {graph.edges()}\n")
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
