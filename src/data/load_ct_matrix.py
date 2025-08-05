'''
src/data/load_ct_matrix.py

Wrapper script for functions pertaining to the loading and saving of the
cortical thickness MRI data. If the data is already saved, it loads the values
from the associated .npy files containing the matrix, filename, and label data,
otherwise loads raw data, arranging into a matrix and returning.

Author:         Benji Lawrence
Last Modified:  05 August 2025
'''
import os
import subprocess
import numpy as np
import pickle
from collections import defaultdict
import nibabel as nib
from src.data.load_config import *

def load_ct_matrix(
    data_dir=DATA_DIR,
    save_dir=SAVE_DIR,
    hemisphere=HEMI_DF,
    reset=False
):
    os.makedirs(save_dir, exist_ok=True)
    T_file = os.path.join(save_dir, T_FILE_DF)
    labels_file = os.path.join(save_dir, LABELS_DF)
    filenames_file = os.path.join(save_dir, FILENAMES_DF)

    # Run fsaverage projection if data_dir doesn't exist or is empty
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        print("Projected data not found. Running fsaverage registration script...")
        subprocess.run(["bash", FSAVG], check=True)

    # Load cached data if available
    if os.path.isfile(T_file) and not reset:
        T = np.load(T_file, allow_pickle=True)
        with open(labels_file, "rb") as f:
            labels = pickle.load(f)
        with open(filenames_file, "rb") as f:
            filenames = pickle.load(f)
        return T, labels, filenames

    T = []
    labels = defaultdict(int)
    filenames = []

    subj_data_dict = defaultdict(list)

    for file in sorted(os.listdir(data_dir)):
        if not file.endswith(".mgh"):
            continue

        parts = file.split(".")
        if len(parts) < 5:
            continue

        subject, hemi, fsavg, _, _ = parts
        if hemisphere != BH and hemi != hemisphere:
            continue

        try:
            data_path = os.path.join(data_dir, file)
            ct_data = nib.load(data_path).get_fdata().squeeze()
        except Exception as e:
            print(f"Failed to read {file}: {e}")
            continue

        subj_data_dict[subject].append(ct_data)

        if subject not in filenames:
            filenames.append(subject)
            labels[subject] = 0 if NC in subject else 1

    for subj in filenames:
        if subj in subj_data_dict:
            thickness_data = np.concatenate(subj_data_dict[subj])
            T.append(thickness_data)

    T = np.vstack(T)
    np.save(T_file, T)
    with open(labels_file, "wb") as f:
        pickle.dump(labels, f)
    with open(filenames_file, "wb") as f:
        pickle.dump(filenames, f)

    return T, labels, filenames

