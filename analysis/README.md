# Ancestral State Reconstruction based on Correspondence Patterns

This project uses correspondence pattern identification in a subset of the NorthPeruLex 
dataset with ≥ 140 concepts in common to infer ancestral states of the sounds through out the trees.

## Instructions to run the workflow

The `analysis` directory where this `README.md` file is located contains two scripts that can be run 
from the command line as ordinary python scripts.
They are written here in order of implementation: (1) `s_aling.py`  and (2) `s_ASR_patterns.py`. 
One can run one script after another as the workflow.
Each one of the scripts fulfills the tasks described next:

1. Load the dataset, 
compute the concept mutual coverage across the data and 
select a subset of languages with a a total of 140 concepts in common, cluster and align the data, and
output the data in a Nexus file for following analysis
2. Automatically infer the correspondence patterns found in the subset and 
perform Sankoff's Maximum Parsimony algorithm for Ancestral State Reconstruction out of the correspondence patterns
to get the proto-sounds