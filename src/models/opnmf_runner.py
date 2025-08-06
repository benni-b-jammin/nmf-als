'''
src/models/opnmf_runner.py

Wrapper program for the OPNMF model used in the ALS categorization program - 
allows for flexibility in switching models if needed.

Author:         Benji Lawrence
Last Modified:  05 August 2025
'''

from opnmf.model import OPNMF 
import numpy as np

def run_opnmf(T, rank, init="nndsvd", max_iter=50000, tol=1e-9, laplacian=None):
    """
    Runs Orthogonal Projective NMF on matrix T.

    Parameters:
    - T: Input data matrix
    - rank: Number of components
    - init: Initialization method
    - max_iter: Maximum number of iterations
    - tol: Convergence tolerance
    - laplacian: Optional manifold Laplacian (not used in your current implementation)

    Returns:
    - W: Basis matrix
    - H: Coefficient matrix
    - V: Reconstruction (W @ H)
    """
    model = OPNMF(n_components=rank, init=init, max_iter=max_iter, tol=tol)
    W = model.fit_transform(T)
    H = model.components_
    V = np.dot(W, H)
    return W, H, V

