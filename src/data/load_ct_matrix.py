'''
src/data/load_ct_matrix.py

Wrapper script for functions pertaining to the loading and saving of the
cortical thickness MRI data. If the data is already saved, it loads the values
from the associated .npy files containing the matrix, filename, and label data,
otherwise loads raw data, arranging into a matrix and returning.

Author:         Benji Lawrence
Last Modified:  26 July 2025
'''
import os
import numpy as np
import pickle
from collections import defaultdict
import nibabel.freesurfer as fs
import load_config # inspect for macro default values

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

    for subj_dir in sorted(os.listdir(data_dir)):
        subj_path = os.path.join(data_dir, subj_dir)
        if not os.path.isdir(subj_path):
            continue

        subj_data = []
        
        # load left hemisphere 
        if hemisphere in (LH, BH):
            lh_path = os.path.join(subj_path, LH_CT_DF)
            if os.path.isfile(lh_path):
                lh_data = fs.read_morph_data(lh_path)
                subj_data.append(lh_data)
            else:
                continue  # skip if missing

        # load right hemisphere
        if hemisphere in (RH, BH):
            rh_path = os.path.join(subj_path, LH_CT_DF)
            if os.path.isfile(rh_path):
                rh_data = fs.read_morph_data(rh_path)
                subj_data.append(rh_data)
            else:
                continue  # skip if missing

        if subj_data:
            thickness = np.concatenate(subj_data)
            T.append(thickness)
            filenames.append(subj_dir)
            labels[subj_dir] = 0 if NC in subj_dir else 1

    T = np.vstack(T)
    np.save(T_file, T)
    with open(labels_file, "wb") as f:
        pickle.dump(labels, f)
    with open(filenames_file, "wb") as f:
        pickle.dump(filenames, f)

    return T, labels, filenames

