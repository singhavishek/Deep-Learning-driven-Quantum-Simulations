# ======================================================================================================================
# Name:                 Simulation Module Function 'HMEX.py'
# Description:          1. This module is designed to create final simulation function.
#                       2. All the components required to run the simulation are called in this module
# Library Dependencies: 1. netket.vqs ("https://netket.readthedocs.io/en/latest/api/vqs.html")
#                       2. netket.optimizer ("https://netket.readthedocs.io/en/latest/api/optimizer.html")
#                       3. netket.driver ("https://netket.readthedocs.io/en/latest/api/drivers.html")
#                       4. netket.logging ("https://netket.readthedocs.io/en/latest/api/logging.html")
# Author:               Avishek Singh
# Date:                 17.05.2022
# Latest Update:        22.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ========= Importing and setting up the libraries =====================================================================
# Importing libraries from netket
from netket.vqs import MCState
from netket.optimizer import SR
from netket.driver import VMC
from netket.logging import RuntimeLog
# ======================================================================================================================

# ====== Main Function =================================================================================================
def hmex(J, h, show_progress_bar: bool = False):
    # ------ Call Lattice Function -------------------------------------------------------------------------------------
    from Function_Tools.Netket_module.lattice import lattice, lattice_info
    graph = lattice()
    lattice_info(graph)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Hilbert Space Function -------------------------------------------------------------------------------
    from Function_Tools.Netket_module.hilbert_space import hilbert_space, hilbert_info
    hilbert = hilbert_space(graph)
    hilbert_info(hilbert)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Hamiltonian Function ---------------------------------------------------------------------------------
    from Function_Tools.Netket_module.hamiltonian import hamiltonian, hamiltonian_info
    ha = hamiltonian(hilbert=hilbert, graph=graph, J=J, h=h)
    hamiltonian_info(ha)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Neural Network Function ------------------------------------------------------------------------------
    from Function_Tools.Netket_module.neural_network import neural_network
    model = neural_network(graph=graph)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Sampling Function ------------------------------------------------------------------------------------
    from Function_Tools.Netket_module.sampler import sampler
    sa = sampler(hilbert=hilbert, graph=graph)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Optimizer Function -----------------------------------------------------------------------------------
    from Function_Tools.Netket_module.optimizer import optimizer
    opt = optimizer()
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Variational Sate Function ---------------------------------------------------------------------------------
    from parameters import samples
    vstate = MCState(sampler=sa, model=model, n_samples=samples)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Observable Function ----------------------------------------------------------------------------------
    from Function_Tools.Observables.observables import observables
    obs = observables(hilbert=hilbert, graph=graph, J=J)
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Call Variational Monte Calo Driver ------------------------------------------------------------------------
    gs = VMC(hamiltonian=ha, optimizer=opt, variational_state=vstate, preconditioner=SR(diag_shift=0.01))
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Creating Runtime Logger Object and Running Simulation -----------------------------------------------------
    from parameters import iterations
    log = RuntimeLog()
    gs.run(n_iter=iterations, out=log, obs=obs, show_progress=show_progress_bar)
    # ------------------------------------------------------------------------------------------------------------------
    return log, list(obs.keys())
# ----------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
