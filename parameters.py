# ======================================================================================================================
# Name:                 Parameter Module 'parameters.py'
# Description:          1. This module contains all the parameters used in the program.
#                       2. To change parameters edit this file.
# Library Dependencies: 1. numpy ("https://numpy.org/")
# Author:               Avishek Singh
# Date:                 18.05.2022
# Latest Update:        20.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ===== Import libraries ===============================================================================================
import numpy as np
# ======================================================================================================================

# ===== Defining the parameters of the simulation ======================================================================
# ------ File Writing Parameters ---------------------------------------------------------------------------------------
source_path = '/home/avishek/Calculations/Neuralnet/Heisenberg_Hamiltonian_in_External_Magnetic_Field/V3/'
path_results = "results/output_files/"       # Define location here to save output files
simulation_file_path = path_results + "simulation_files/"     # Define location here to save simulation files
var_file_path = path_results + "combined_var_data_files/"     # Define location here to save variable files
J_parsed_file_path = path_results + "J_parsed_files/"         # Define location here to save J parsed files
fitting_param_path = path_results + "fitting_param_files/"    # Define location here to save fitting param files
# ----------------------------------------------------------------------------------------------------------------------

# ------ Graph Plotting Parameters -------------------------------------------------------------------------------------
path_plots = "results/plots/"
parsed_data_plot_path = path_plots + "parsed_data_plots/"
fitted_plot_path = path_plots + "fitted_plots/"
J_parsed_plot_path = path_plots + "j_parsed_plots/"
# ----------------------------------------------------------------------------------------------------------------------

# ----- Runtype Environment Parameters ---------------------------------------------------------------------------------
run_type = 'cpu'
# ----------------------------------------------------------------------------------------------------------------------

# ----- Lattice parameters ---------------------------------------------------------------------------------------------
lattice_type = "hypercube"   # Type of lattice: "hypercube" or "custom"
pbc = True                   # Periodic boundary conditions, Set False for Open Boundary
if lattice_type == "hypercube":
    length = 4
    dim = 2
elif lattice_type == "custom":
    # Basis Vectors that define the positioning of the unit cell
    basis_vectors = [[0, 1], [np.sqrt(3)/2, -1/2]]
    # Locations of atoms within the unit cell
    atomic_positions = [[0, 0], [np.sqrt(3)/6, 1/2]]
    # Number of unit cells in each direction
    dimensions = [3, 3]
    # Default PointGroup object for constructing space groups
    point_group = None        # specify a point group to use
    # Max Nearest Neighbour Order
    neighbor_order = None     # specify a neighbor order to use, By Default it is set to 1.
else:
    raise ValueError("Lattice type not recognized")
write_lattice_info = True       # Write lattice information to file "lattice_Info.txt"
print_lattice_info = False      # Print lattice information to screen
path_to_lattice_info = path_results + "QSfiles/"     # Path to write lattice information to file
# ----------------------------------------------------------------------------------------------------------------------

# ----- Hilbert Space Parameters ---------------------------------------------------------------------------------------
hilbert_space_type = "spin"  # Type of Hilbert Space: "spin" or "fock"
if hilbert_space_type == "spin":
    s = 1/2
    total_sz = None        # constrains the total spin of system to a particular value: Set to "None" for no constraint
elif hilbert_space_type == "fock":   # For Boson Hilbert Space (Fock Basis) calculations
    n_max = None           # Maximum occupation for a site. If "None", the local occupation number is unbounded.
    N = 3                 # Number of bosonic modes
    n_particles = None    # Constraint for the number of particles. If "None", no constraint is imposed.
else:
    raise ValueError("Hilbert Space type not recognized")
write_hilbert_info = True  # Write hilbert space information to file "hilbert_Info.txt"
print_hilbert_info = False  # Print hilbert space information to screen
path_to_hilbert_info = path_results + "QSfiles/"  # Path to hilbert space information file
# ----------------------------------------------------------------------------------------------------------------------

# ----- Hamiltonian parameters -----------------------------------------------------------------------------------------
# Parameters for the Hamiltonian can take one value or range of values.
# You can specify the parameters for prebuilt Hamiltonian in 'netket.operator' module here and import as required.
h_ex = [0.0, 6]      # Range of h values to be tested. [start value, end value]. It also takes a single value.
h_ex_increment = 0.06  # Increment over h_ex range
J_ex = [-1, -2]        # Range of J values to be tested. [start value, end value]
J_ex_increment = 0.5     # Increment over J_ex range
write_hamiltonian_info = True  # Write hamiltonian information to file "hamiltonian_Info.txt"
print_hamiltonian_info = False  # Print hamiltonian information to screen
path_to_hamiltonian_info = path_results + "QSfiles/"  # Path to hamiltonian information file
# ----------------------------------------------------------------------------------------------------------------------

# ----- Neural Network Parameters --------------------------------------------------------------------------------------
neural_network_type = "DenseFFNN"  # Type of Neural Network: "DenseFFNN" or "DenseFFNN_sym" or "G-CNN"
if neural_network_type == "DenseFFNN":
    pass
elif neural_network_type == "DenseFFNN_sym":
    alpha = 4                      # Features per symmetry
elif neural_network_type == "G-CNN":
    feature_dims = [8, 8, 8, 8]    # Feature dimensions of hidden layers, from first to last
    num_layers = 4                 # Number of layers
else:
    raise ValueError("Neural Network type not recognized")
# ----------------------------------------------------------------------------------------------------------------------

# ------ Monte Carlo Sampler Parameters --------------------------------------------------------------------------------
sampler_type = "Local"    # Type of Sampler: "Local" or "Exchange"
n_chains_per_rank = None  # Number of independent chains on every MPI rank. If "None", takes default value (=16).
machine_pow = None        # The power to which the machine should be exponentiated. If "None", takes default value (=2).
if sampler_type == "Local":
    pass
elif sampler_type == "Exchange":
    d_max = 1             # The maximum graph distance allowed for exchanges.
else:
    raise ValueError("Sampler type not recognized")
# ----------------------------------------------------------------------------------------------------------------------

# ------ Optimizer Parameters ------------------------------------------------------------------------------------------
optimizer_type = "Sgd"  # Type of Optimizer: "Sgd" or "AdaGrad" or "Adam"
learning_rate = 0.01     # Learning rate
if optimizer_type == "Sgd":
    pass
elif optimizer_type == "AdaGrad":
    epscut = 1e-6                    # Small 'epsilon' cutoff
    initial_accumulator_value = 0.1  # Initial value for the accumulator
elif optimizer_type == "Adam":
    beta1 = 0.9          # Decay rate for the exponentially weighted average of grads.
    beta2 = 0.999        # Decay rate for the exponentially weighted average of squared norm of grads.
    eps = 1e-8           # Term added to the denominator to improve numerical stability.
else:
    raise ValueError("Optimizer type not recognized")
# ----------------------------------------------------------------------------------------------------------------------

# ------ Variational Monte Carlo Parameters ----------------------------------------------------------------------------
iterations = 300
samples = 512
# ----------------------------------------------------------------------------------------------------------------------

# ----- Miscellaneous --------------------------------------------------------------------------------------------------
n_values = 20
# ----------------------------------------------------------------------------------------------------------------------
