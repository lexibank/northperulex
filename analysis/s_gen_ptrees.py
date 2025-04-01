"""
This script generates phylogenetic trees using the
Neighbor-Joining (Saitou and Nei 1987) algorithm.
"""

import os
import re
from lingpy.algorithm.clustering import neighbor

output_directory = 'trees'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

cognate_sets = []
with open("distance_matrix.tsv", "r") as f:
    lines = f.readlines()
    
current_cogid = None
labels = []
matrix = []

for line in lines:
    line = line.strip()
    if line.startswith("Cogid:"):
        if current_cogid is not None:
            cognate_sets.append((current_cogid, labels, matrix))
    
        current_cogid = line.split(":")[1].strip()
        labels = []
        matrix = []
        
    elif line and not labels:
        labels = [re.sub(": ", "_", item) for item in line.split("\t")]
        labels = ["".join(label.split()) for label in labels]
        
    elif line:
        parts = line.split("\t")
        distances = [float(val) for val in parts[1:]]
        matrix.append(distances)
        
if current_cogid is not None:
    cognate_sets.append((current_cogid, labels, matrix))

saved_trees = 0
skipped_trees = 0

for cogid, labels, matrix in cognate_sets:
    if len(matrix) != len(labels):
        skipped_trees += 1
        continue
    
    newick_tree = neighbor(matrix, labels)
    
    output_filename = os.path.join(output_directory, f"tree_cogid{cogid}.nwk")
    with open(output_filename, "w") as f:
        f.write(newick_tree)
    saved_trees += 1