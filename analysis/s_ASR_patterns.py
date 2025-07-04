from lingpy import *
import os
from lingrex.util import add_structure
from lingrex.copar import CoPaR, consensus_pattern
from collections import defaultdict
from lingpy.compare.strings import ldn_swap, bidist2, tridist2
from lingpy.algorithm.clustering import neighbor
import numpy as np
from pylotree import Tree, NodeLabels
from pyloparsimony import up, down, parsimony
from pyloparsimony.util import scenario_ascii_art
import newick

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
        
# Build trees
# Get the distance matrices
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
    
    # Apply NJ for trees construction
    nwk_tree = neighbor(dist_matrix, taxa)
    parsed_newick = newick.loads(nwk_tree)
    # Handling trees
    parsed_tree = Tree(nwk_tree, name=f"{key[0]}_{key[1]}")
    labeled_tree = parsed_tree.newick
    
    # Output tree
    output_filename = os.path.join(
        output_directory, f"tree_cogid{key[0]}_slot{key[1]}.nwk"
    )
    with open(output_filename, "w") as f:
        f.write(labeled_tree)
    
    # Maximum Parsimony algorithm for ancestral state reconstruction
    pattern = {
        f"{doc}_{sound}": [sound]
        for doc, sound in doc_sound_pairs
    }
    characterlist = sorted(set([sound for _, sound in doc_sound_pairs]))
    #print(characterlist)
        
    matrix_dict = {
        (i, j): matrix[i][j]
        for i in range(len(filtered_sounds))
        for j in range(len(filtered_sounds))
    }
    sound_index = {sound: i for i, sound in enumerate(filtered_sounds)}
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
        
    # Computer costs UP and DOWN the tree
    W = up(
        parsed_tree,
        characterlist,
        penalty_matrix,
        pattern
    )
    scenarios = down(
        parsed_tree,
        characterlist,
        penalty_matrix,
        W
    )
    
    best = scenarios[0]
    tree_art = scenario_ascii_art(best, parsed_tree)
    print(tree_art)