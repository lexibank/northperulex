from lingpy import *
from lingrex.util import add_structure
from lingrex.copar import CoPaR, consensus_pattern
from collections import defaultdict
from lingpy.compare.strings import ldn_swap, bidist2, tridist2
from tabulate import tabulate
from lingpy.algorithm.clustering import neighbor
from lingpy.thirdparty.cogent.newick import parse_string
import numpy as np
from pylotree import Tree
from pyloparsimony.util import matrix_from_chars
import copy
from pyloparsimony import up, down

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
            matrix[i, j] = 1 - combined_distance # similarity
            
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

#print(cop.patterns.items())

# Get consensus patterns
pattern_dict = defaultdict(list)
for key, pattern_list in cop.patterns.items():
    for pattern in pattern_list:
        pattern_dict[key].append(pattern[2])
        
consensus_patterns = {}
for key, patterns in pattern_dict.items():
    try:
        consensus = consensus_pattern(patterns, missing="Ø")
        consensus_patterns[key] = consensus
    except ValueError:
        print(f"Incompatible patterns at {key}")
        
#print(consensus_patterns.items())

# Getting the similarity matrices
for key, values in consensus_patterns.items():
    filtered, matrix = compute_matrix(values)
    headers = [""] + filtered
    table = [[filtered[i]] + [f"{val:.2f}" for val in matrix[i]] for i in range(len(filtered))]
    print(f"\nCOGID={key[0]} | SLOT={key[1]}:")
    print(tabulate(table, headers=headers, tablefmt="plain"))
    
#
    