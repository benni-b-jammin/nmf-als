'''
src/visual/plot_to_brain.py

Script to visualize cortical thickness on a brain mesh, including main
functions for mapping as well as helper functions for plotting. This script is
based on previous work by Khoi Nguyen Xuan adapted for my use case.

Author:         Benji Lawrence, Khoi Nguyen Xuan
Last Modified:  01 August 2025
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import nibabel.freesurfer as fs
import trimesh

def visualize_ct(
    thickness_path: str,
    mesh_path: str,
    cmap_name: str = "plasma",
    show_colorbar: bool = True,
    show_mesh: bool = True,
):
    """
    Visualizes cortical thickness on a brain surface mesh.

    Parameters:
    - thickness_path: Path to .thickness file (e.g., lh.thickness)
    - mesh_path: Path to .pial file (e.g., lh.pial)
    - cmap_name: Name of matplotlib colormap (default: plasma)
    - show_colorbar: Whether to display the colorbar
    - show_mesh: Whether to display the mesh in an external viewer
    """

    # Load thickness and mesh data
    thickness_data = fs.read_morph_data(thickness_path)
    coords, faces = fs.read_geometry(mesh_path)

    # Reshape faces if necessary
    if faces.ndim == 1:
        faces = faces.reshape((-1, 3))

    # Normalize thickness to [0, 1]
    norm_thickness = (thickness_data - np.min(thickness_data)) / (np.max(thickness_data) - np.min(thickness_data))

    # Apply colormap
    cmap = cm.get_cmap(cmap_name)
    colors = (cmap(norm_thickness)[:, :3] * 255).astype(np.uint8)

    # Create and show mesh
    mesh = trimesh.Trimesh(vertices=coords, faces=faces, vertex_colors=colors, process=False)

    if show_colorbar:
        _plot_colorbar(thickness_data, cmap, label="Cortical Thickness (mm)")

    if show_mesh:
        mesh.show()

    return mesh  # Optionally return for saving/exporting/etc.

def _plot_colorbar(data, cmap, label=""):
    """Utility function to plot a horizontal colorbar."""
    fig, ax = plt.subplots(figsize=(6, 1.2))
    fig.subplots_adjust(bottom=0.5)

    norm = plt.Normalize(vmin=np.min(data), vmax=np.max(data))
    cb = plt.colorbar(
        cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=ax,
        orientation='horizontal'
    )
    cb.set_label(label, fontsize=10)
    plt.show()

