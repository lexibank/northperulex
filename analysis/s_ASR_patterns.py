"""
This script calculates the correspondence patterns
found in the data and computes a cost matrix of the
changes between each character state and each other
state to perform Sankoff's Maximum Parsimony
algorithm for Ancestral State Reconstruction
"""

from lingpy import *
import os
from collections import Counter
from lingrex.util import add_structure
from lingrex.copar import CoPaR, consensus_pattern
from commonnexus import Nexus
from pyloparsimony import up, down, parsimony
from pyloparsimony.util import scenario_ascii_art
from pylotree import Tree, NodeLabels

#output_directory = 'CP_trees'
#if not os.path.exists(output_directory):
#os.makedirs(output_directory)

# Retrieve input species tree
nex = Nexus.from_file("npl.nex.con.tre")
translated_tree = nex.TREES.translate(nex.TREES.TREE)
translated_tree.visit(NodeLabels(node_name_prefix='Edge', root_name='Root'))
tree = Tree(translated_tree)

# Load and align data
alms = Alignments("npl.tsv", ref="cogids", transcription="form")
alms.align()
add_structure(alms, model="cv")
alms.output('tsv', filename="npl-aligned", ignore="all", prettify=False)

# Get the correspondence patterns
cop = CoPaR("npl-aligned.tsv", min_refs=5, ref='cogids', transcription="form")
cop.get_sites()
cop.cluster_sites()
cop.sites_to_pattern()
cop.add_patterns()
cop.write_patterns("npl-patterns.tsv")

# Prioritize more recurrent patterns
valid_patterns = {key: sites for key, sites in cop.patterns.items() if len(sites) > 1}
consensus_patterns = {}

for (cogid, slot), site_list in valid_patterns.items():
    patterns = [pattern[2] for pattern in site_list]
    try:
        consensus = consensus_pattern(patterns, missing="Ø")
    except ValueError:  # Except, pick the most frequent value
        consensus = []
        for col in zip(*patterns):
            no_gaps = [x for x in col if x != "Ø"]
            consensus.append(Counter(no_gaps).most_common(1)[0][0] if no_gaps else "Ø")
        consensus = tuple(consensus)
    
    consensus_patterns[(cogid, slot)] = {
        doculect: char for doculect, char in zip(cop.cols, consensus)
    }
    
leaves = [leaf.name for leaf in tree.root.walk() if leaf.is_leaf]

# Compute costs UP and DOWN the tree for each pattern
for (cogid, slot), pattern in consensus_patterns.items():
    characterlist = sorted(set(pattern.values()))
    print(f"Running Sankoff on {(cogid, slot)}")
    
    # Define penalty matrix
    penalty_matrix = []
    for c1 in characterlist:
        row = []
        for c2 in characterlist:
            if c1 == c2:
                cost = 0.0
            elif c1 == '-':
                cost = 2.0  # Gain is more costly
            elif c2 == '-':
                cost = 1.0  # Loss is less costly
            else:
                cost = 1.0  # Substitution
            row.append(cost)
        penalty_matrix.append(row)
        
    W = up(
        tree,
        characterlist,
        penalty_matrix,
        pattern
    )
    
    scenarios = down(
        tree,
        characterlist,
        penalty_matrix,
        W
    )
    
    best = scenarios[0]
    tree_art = scenario_ascii_art(best, tree)
    print(tree_art)
