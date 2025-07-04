# Ancestral State Reconstruction based on Correspondence Patterns

This project uses correspondence pattern identification in a subset of the NorthPeruLex dataset with ≥ 140 concepts in common to infer ancestral states of the sounds through out the trees.

## Instructions to run the workflow

The `analysis` directory where this `README.md` file is located contains three scripts that can be run from the command line as ordinary python scripts.
They are written here in order of implementation: (1) `s_aling.py`, (2) `s_subsampling.py`, and (3) `s_ASR_patterns.py`. 
One can run one script after another as the workflow.
Each one of the scripts fulfills a task described next:

1. Load the dataset and cluster and align the data
2. Compute the concept mutual coverage across the data and select a subset of languages with a a total of 140 concepts in common
3. Automatically infer the correspondence patterns found in the subset and perform Sankoff's Maximum Parsimony algorithm for Ancestral State Reconstruction out of the correspondence patterns