'''
src/models/nmf_runner.py

Wrapper program for the NMF model used in the ALS categorization program - 
allows for flexibility in switching models if needed.

Author:         Benji Lawrence
Last Modified:  25 July 2025
'''

from sklearn.decomposition import NMF
import numpy as np

def run_nmf(T, rank, init="nndsvd", max_iter=50000, tol=1e-9, random_state=0):
    """
    Runs standard NMF on matrix T.

    Parameters:
    - T: Input data matrix (n_samples x n_features)
    - rank: Number of components
    - init: Initialization method ('random', 'nndsvd', etc.)
    - max_iter: Maximum number of iterations
    - tol: Convergence tolerance

    Returns:
    - W: Basis matrix (n_samples x rank)
    - H: Coefficient matrix (rank x n_features)
    - V: Reconstruction matrix (W @ H)
    """
    model = NMF(n_components=rank, init=init, max_iter=max_iter,
                tol=tol, random_state=random_state)
    W = model.fit_transform(T)
    H = model.components_
    V = np.dot(W, H)
    return W, H, V
