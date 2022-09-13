# ======================================================================================================================
# Name:                 Neural Network Optimization Module 'optimizer.py'
# Description:          This module contains function to construct neural network optimizer.
# Library Dependencies: 1. Netket_module.optimizer ("https://netket.readthedocs.io/en/latest/api/optimizer.html")
# Author:               Avishek Singh
# Date:                 17.05.2022
# Latest Update:        18.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
from netket import optimizer
from netket.optimizer import Sgd, AdaGrad, Adam
# ======================================================================================================================

# ====== Defining Lattice Functions ====================================================================================
# ------ Defining a function to create a lattice -----------------------------------------------------------------------
def optimizer() -> optimizer:
    from parameters import optimizer_type, learning_rate
    if optimizer_type == 'Sgd':
        return Sgd(learning_rate=learning_rate)
    elif optimizer_type == 'AdaGrad':
        from parameters import epscut, initial_accumulator_value
        return AdaGrad(learning_rate=learning_rate, epscut=epscut, initial_accumulator_value=initial_accumulator_value)
    elif optimizer_type == 'Adam':
        from parameters import beta1, beta2, eps
        return Adam(learning_rate=learning_rate, b1=beta1, b2=beta2, eps=eps)
    else:
        raise ValueError("Optimizer type not found. Please check the optimizer type in the parameters.py file.")
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
