from lingpy import *
import os
from lingrex.util import add_structure
from lingrex.copar import CoPaR, consensus_pattern
from collections import defaultdict
from lingpy.compare.strings import ldn_swap, bidist2, tridist2
from lingpy.algorithm.clustering import neighbor
from lingpy.thirdparty.cogent.newick import parse_string
import numpy as np
from pylotree import Tree, NodeLabels
import copy
from pyloparsimony import up, down

output_directory = 'CP_trees'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def compute_matrix(symbols):
    """This function computes the similarity matrix for each correspondence pattern
    out of Levenstein distance with swap included."""
    filtered = [s for s in symbols if s != 'Ø']
    n = len(filtered)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            levenshtein_distance = ldn_swap(filtered[i], filtered[j], normalized=True)
            bigram_distance = bidist2(filtered[i], filtered[j], normalized=True)
            trigram_distance = tridist2(filtered[i], filtered[j], normalized=True)
            combined_distance = (
                    0.34 * levenshtein_distance +
                    0.33 * bigram_distance +
                    0.33 * trigram_distance
            )
            matrix[i, j] = combined_distance
            
    return filtered, matrix
    

# Get the patterns
alms = Alignments("npl_filtered.tsv", ref="cogids", transcription="form")
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
pattern_dict = defaultdict(list)
for key, pattern_list in cop.patterns.items():
    for pattern in pattern_list:
        sounds = pattern[2]
        for doculect, sound in zip(cop.cols, sounds):
            pattern_dict[key].append((doculect, sounds))
        
consensus_patterns = {}
doculect_sounds_mappings = {}
for key, docusound_list in pattern_dict.items():
    sounds = [s for _, s in docusound_list]
    doculects = [d for d, _ in docusound_list]
    try:
        consensus = consensus_pattern(sounds, missing="Ø")
        consensus_patterns[key] = consensus
        doculect_sounds_mappings[key] = [
            f"{doc}_{sound}" for doc, sound in zip(doculects, sounds) if sound != "Ø"
        ]
    except ValueError:
        print(f"Incompatible patterns: {key}")
        

# Getting the similarity matrices
for key, values in consensus_patterns.items():
    doc_sound_pairs = [
        (doc, sound) for doc, sound in zip(cop.cols, values) if sound != "Ø"
    ]
    if len(doc_sound_pairs) < 2:
        continue
    taxa = [f"{doc}_{sound}" for doc, sound in doc_sound_pairs]
    sounds = [sound for _, sound in doc_sound_pairs]

    filtered_sounds, matrix = compute_matrix(sounds)

    if len(filtered_sounds) != len(taxa) or matrix.shape[0] != len(taxa):
        continue

    headers = [""] + taxa
    table = [
        [taxa[i]] + [f"{val:.2f}" for val in matrix[i]]
        for i in range(len(taxa))
    ]

    dist_matrix = matrix.tolist()
    nwk_tree = neighbor(dist_matrix, taxa)
    
        
    parsed_tree = Tree(nwk_tree, name=f"{key[0]}_{key[1]}")
    labeled_tree = parsed_tree.newick

    output_filename = os.path.join(
        output_directory, f"tree_cogid{key[0]}_slot{key[1]}.nwk"
    )
    with open(output_filename, "w") as f:
        f.write(labeled_tree)