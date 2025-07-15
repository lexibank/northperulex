from lingpy import *
import os
from lingrex.util import add_structure
from lingrex.copar import CoPaR, consensus_pattern, score_patterns
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

# Get consensus patterns
for key, pattern_list in cop.patterns.items():
    patterns = [p[2] for p in pattern_list]
    score = score_patterns(patterns, missing="Ø", mode='coverage')
    if score > -1:
        print(key, score)
    else:
        continue
    #try:
    #    consensus = consensus_pattern(patterns, missing="Ø")
    #except ValueError:
    #    continue
        
        

    