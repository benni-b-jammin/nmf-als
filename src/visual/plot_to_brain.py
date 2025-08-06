'''
src/visual/plot_to_brain.py

Script to visualize cortical thickness on a brain mesh, including main
functions for mapping as well as helper functions for plotting. This script is
based on previous work by Khoi Nguyen Xuan adapted for my use case.

Author:         Benji Lawrence, Khoi Nguyen Xuan
Last Modified:  05 August 2025
'''
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import trimesh
import nibabel.freesurfer as fs
import nibabel as nib


def visualize_ct(
    subject_id: str = None,
    data_dir: str = None,
    hemi: str = "bh",
    fsaverage_dir: str = os.path.expanduser("~/freesurfer/freesurfer/subjects/fsaverage5/surf"),
    surface: str = "inflated",
    cmap_name: str = "plasma",
    show_colorbar: bool = True,
    H_row: np.ndarray = None,
):
    """
    Visualizes cortical thickness from a file OR from a row in the NMF H matrix on the fsaverage surface.

    Parameters:
    - subject_id: Subject ID prefix (only needed if using .mgh file)
    - data_dir: Directory with .mgh files
    - hemi: Hemisphere to show: 'lh', 'rh', or 'bh'
    - fsaverage_dir: Path to fsaverage5 surface directory
    - surface: 'inflated', 'pial', or other FreeSurfer surface
    - cmap_name: Matplotlib colormap
    - show_colorbar: Whether to include a colorbar
    - H_row: A row from H matrix (used instead of file input)
    """

    if hemi not in {"lh", "rh", "bh"}:
        raise ValueError("hemi must be 'lh', 'rh', or 'bh'")

    if H_row is None and (subject_id is None or data_dir is None):
        raise ValueError("Either H_row or (subject_id + data_dir) must be provided.")

    mesh_list = []
    all_thickness = []

    hemispheres = ["lh", "rh"] if hemi == "bh" else [hemi]
    vtx_count = 10242  # vertices per hemisphere for fsaverage5

    for idx, h in enumerate(hemispheres):
        surf_path = os.path.join(fsaverage_dir, f"{h}.{surface}")

        if not os.path.isfile(surf_path):
            print(f"Surface file not found: {surf_path}")
            continue

        # Get cortical thickness data
        if H_row is not None:
            # Use data from H matrix
            start = idx * vtx_count
            end = (idx + 1) * vtx_count
            if len(H_row) < end:
                print(f"Not enough values in H_row to visualize {h}")
                continue
            thickness_data = H_row[start:end]
        else:
            # Use data from file
            mgh_path = os.path.join(data_dir, f"{subject_id}.{h}.fsaverage5.thickness.mgh")
            if not os.path.isfile(mgh_path):
                print(f"MGH file not found: {mgh_path}")
                continue
            thickness_data = nib.load(mgh_path).get_fdata().squeeze()

        # Load surface and colorize
        coords, faces = fs.read_geometry(surf_path)
        if faces.ndim == 1:
            faces = faces.reshape((-1, 3))

        # Normalize thickness and map to color
        norm_thickness = (thickness_data - np.min(thickness_data)) / (np.max(thickness_data) - np.min(thickness_data) + 1e-6)
        cmap = cm.get_cmap(cmap_name)
        colors = (cmap(norm_thickness)[:, :3] * 255).astype(np.uint8)

        # Create trimesh
        mesh = trimesh.Trimesh(vertices=coords, faces=faces, vertex_colors=colors, process=False)
        mesh_list.append(mesh)
        all_thickness.append(thickness_data)

    if not mesh_list:
        raise RuntimeError("No valid surface or data found to visualize.")

    # Show using trimesh default viewer (opens in external window)
    for mesh in mesh_list:
        mesh.show()

    # Plot colorbar
    if show_colorbar:
        _plot_colorbar(np.concatenate(all_thickness), cm.get_cmap(cmap_name), label="Cortical Thickness (mm)")

    return mesh_list


def _plot_colorbar(data, cmap, label="Cortical Thickness (mm)"):
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

