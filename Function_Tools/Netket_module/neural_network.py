# ======================================================================================================================
# Name:                 Artificial Neural Network Construction Module 'neural_network.py'
# Description:          This module contains functions for constructing Neural Networks.
# Library Dependencies: 1. Netket_module.nn ("https://netket.readthedocs.io/en/latest/api/graph.html")
#                       2. Netket_module.models ("https://netket.readthedocs.io/en/latest/api/models.html")
#                       3. jax ("https://jax.readthedocs.io/en/latest/index.html")
#                       4. numpy ("https://numpy.org/")
#                       5. jax.numpy ("https://jax.readthedocs.io/en/latest/jax-101/01-jax-basics.html?highlight=numpy")
# Author:               Avishek Singh
# Date:                 19.05.2022
# Latest Update:        19.05.2022
# Version:              1.0.0
# ======================================================================================================================

# ====== Importing Libraries ===========================================================================================
import netket.nn as nknn
import jax.numpy as jnp
import jax
import numpy as np
# ======================================================================================================================

# ====== Defining Neural Network Functions =============================================================================
# ------ Defining a function to create a Neural Network ----------------------------------------------------------------
def neural_network(graph) -> nknn:
    from parameters import neural_network_type
    if neural_network_type == 'DenseFFNN':
        class FFNN(nknn.Module):
            @nknn.compact
            def __call__(self, x):
                x = nknn.Dense(features=2 * x.shape[-1], use_bias=True, dtype=np.complex128,
                               kernel_init=jax.nn.initializers.normal(stddev=0.1),
                               bias_init=jax.nn.initializers.normal(stddev=0.1))(x)
                x = nknn.log_cosh(x)
                x = jnp.sum(x, axis=-1)
                return x
        return FFNN()
    elif neural_network_type == 'DenseFFNN_sym':
        from parameters import alpha
        class FFNN_sym(nknn.Module):
            _alpha: int
            @nknn.compact
            def __call__(self, x):
                x = nknn.Dense(symmetries=graph.translation_group(), features=self._alpha, use_bias=True,
                               dtype=np.complex128, kernel_init=jax.nn.initializers.normal(stddev=0.1),
                               bias_init=jax.nn.initializers.normal(stddev=0.1))(x)
                x = nknn.log_cosh(x)
                x = jnp.sum(x, axis=(-1, -2))
                return x
        return FFNN_sym(_alpha=alpha)
    elif neural_network_type == 'G-CNN':
        from parameters import feature_dims, num_layers
        from netket.models import GCNN
        return GCNN(symmetries = graph.automorphisms(), layers = num_layers, features = feature_dims)
    else:
        raise ValueError('Neural Network Type not defined.')
# ======================================================================================================================
