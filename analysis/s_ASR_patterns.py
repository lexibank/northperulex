from lingpy import *
import os
import csv
from collections import Counter
from lingrex.util import add_structure
from lingrex.copar import CoPaR, consensus_pattern
from collections import defaultdict
from lingpy.algorithm.clustering import neighbor
from lingpy.basic.tree import random_tree
import numpy as np
from pylotree import Tree, NodeLabels
from pyloparsimony import up, down, parsimony
from pyloparsimony.util import scenario_ascii_art
import newick

output_directory = 'CP_trees'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
output_matrices = 'presence_absence_matrices'
os.makedirs(output_matrices, exist_ok=True)


# Get the patterns
alms = Alignments("npl.tsv", ref="cogids", transcription="form")
alms.align()
add_structure(alms, model="cv")
alms.output('tsv', filename="npl-aligned", ignore="all", prettify=False)

cop = CoPaR("npl-aligned.tsv", min_refs=5, ref='cogids', transcription="form")
cop.get_sites()
cop.cluster_sites()
cop.sites_to_pattern()
cop.add_patterns()
cop.write_patterns("npl-patterns.tsv")

# Get patterns
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
            if not no_gaps:
                consensus.append("Ø")
            else:
                most_common = Counter(no_gaps).most_common(1)[0][0]
                consensus.append(most_common)
        consensus = tuple(consensus)
    
    consensus_patterns[(cogid, slot)] = consensus
        
    