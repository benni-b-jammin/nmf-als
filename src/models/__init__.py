'''
src/models/__init__.py

Init file for (OP)NMF models

Author:         Benji Lawrence
Last Modified:  25 July 2025
'''
from .nmf_runner import run_nmf
from .opnmf_runner import run_opnmf

__all__ = ["run_nmf", "run_opnmf"]

