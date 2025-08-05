'''
src/data/load_config.py

Config file for adjusting standing data information for loading cortical
thickness data, including standard file and directory names.

Author:         Benji Lawrence
Last Modified:  05 August 2025
'''

# Hemisphere types
LH = "lh"
RH = "rh"
BH = "bh"

# Default inputs (Data Directories, Hemisphere Type)
DATA_DIR        = "./data/raw/subjects/fsa_results/"
SAVE_DIR        = "./data/saved/"
HEMI_DF         = LH    #TODO change when needed

# Default Filenames
T_FILE_DF       = "T.npy"
LABELS_DF       = "labels.npy"
FILENAMES_DF    = "filenames.npy"
LH_CT_DF        = "lh.thickness"
RH_CT_DF        = "rh.thickness"

# Script for register fsaverage
FSAVG = "./src/data/register_fsaverage.sh"

# Filetypes: NC or AD
NC = "NC"
AD = "AD"
