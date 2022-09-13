# ======================================================================================================================
# Name:                 Sampler Construction Module 'sampler.py'
# Description:          This module contains functions for constructing Monte Carlo Sampler.
# Library Dependencies: 1. Netket_module.sampler ("https://netket.readthedocs.io/en/latest/api/sampler.html")
# Author:               Avishek Singh
# Date:                 19.05.2022
# Latest Update:        19.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
import netket.sampler as nk_sampler
from netket.sampler import MetropolisLocal, MetropolisExchange
# ======================================================================================================================

# ====== Defining Sampler Functions ====================================================================================
# ------ Defining a function to create a sampler -----------------------------------------------------------------------
def sampler(hilbert, graph) -> nk_sampler:
    from parameters import sampler_type, n_chains_per_rank, machine_pow
    if sampler_type == "Local":
        if n_chains_per_rank is None and machine_pow is None:
            return MetropolisLocal(hilbert=hilbert)
        elif n_chains_per_rank is not None and machine_pow is not None:
            return MetropolisLocal(hilbert=hilbert, n_chains_per_rank=n_chains_per_rank, machine_pow=machine_pow)
        elif n_chains_per_rank is None and machine_pow is not None:
            return MetropolisLocal(hilbert=hilbert, machine_pow=machine_pow)
        elif n_chains_per_rank is not None and machine_pow is None:
            return MetropolisLocal(hilbert=hilbert, n_chains_per_rank=n_chains_per_rank)
        else:
            raise ValueError("Please provide either n_chains_per_rank or machine_pow.")
    elif sampler_type == "exchange":
        from parameters import d_max
        if n_chains_per_rank is None and machine_pow is None:
            return MetropolisExchange(hilbert=hilbert, graph=graph, d_max=d_max)
        elif n_chains_per_rank is not None and machine_pow is not None:
            return MetropolisExchange(hilbert=hilbert, graph=graph, d_max=d_max, n_chains_per_rank=n_chains_per_rank,
                                      machine_pow=machine_pow)
        elif n_chains_per_rank is None and machine_pow is not None:
            return MetropolisExchange(hilbert=hilbert, graph=graph, d_max=d_max, machine_pow=machine_pow)
        elif n_chains_per_rank is not None and machine_pow is None:
            return MetropolisExchange(hilbert=hilbert, graph=graph, d_max=d_max, n_chains_per_rank=n_chains_per_rank)
        else:
            raise ValueError("Please provide either n_chains_per_rank or machine_pow.")
    else:
        print("Sampler type not recognized. Please choose either local or exchange.")
        return
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
