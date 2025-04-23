import csv
import os
import math
from ete3 import Tree

# Load trees
tree_dir = 'trees'
tree_files = [f for f in os.listdir(tree_dir) if f.endswith('.nwk')]

trees = {}
for file in tree_files:
    filepath = os.path.join(tree_dir, file)
    cogid = os.path.splitext(file)[0].split('cogid', 1)[1]
    tree = Tree(filepath, format=1)
    for leaf in tree.iter_leaves():
        if '_' in leaf.name:
            leaf.name = leaf.name.split('_', 1)[1]
    trees[cogid] = tree
    

# Load data
data = []
with open('npl_copped.tsv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    for i, row in enumerate(reader):
        if i < 3 or (len(row) > 0 and row[0].startswith('#')):
            continue
        data.append(row)

# Group by COGID
cogid_data = {}
for row in data[1:]:
    cogid = row[21]
    alignment = row[23].split()
    form = row[5]
    if cogid not in cogid_data:
        cogid_data[cogid] = []
    cogid_data[cogid].append((form, alignment))

#if '2' in cogid_data:
    #for alignment in cogid_data['2']:
        #print(f"{alignment}")
        
def get_states(cogid_data):
    states = set()
    for alignments in cogid_data.values():
        for _, alignment in alignments:
            states.update(alignment)
    return sorted(states)

# Sankoff algorithm
def sankoff_parsimony(tree, alignment, states):
    """
    This is the function for the ancestral state reconstruction implementing
    Sankoff's algorithm for maximum parsimony.
    """
    # terminal leaves, internal nodes in the tree
    # slots within the alignment
    state_costs = {}
    
    # Assign costs to leaves
    def unit_cost(i, j):
        return 0 if i == j else 1

    for node in tree.traverse("postorder"):
        costs = {}
        if node.is_leaf():
            observed = alignment.get(node.name, None)
            for s in states:
                costs[s] = 0 if s == observed else math.inf
        else:
            children = node.get_children()
            c1_costs = state_costs[children[0]]
            c2_costs = state_costs[children[1]]
            for s in states:
                c1 = min(unit_cost(s, j) + c1_costs[j] for j in states)
                c2 = min(unit_cost(s, j) + c2_costs[j] for j in states)
                costs[s] = c1 + c2
        state_costs[node] = costs
    return state_costs
    
    # Compute costs bottom up

# Run everything

all_states = get_states(cogid_data)

for cogid, tree in trees.items():
    if cogid not in cogid_data:
        continue
        
    leaf_to_alignment = {}
    leaves = [leaf.name for leaf in tree.iter_leaves()]
    alignment_pool = [(i, ''.join(aln), aln) for i, (_, aln) in enumerate(cogid_data[cogid])]
    used_indices = set()
    unmatched_leaves = []
    
    for leaf in tree.iter_leaves():
        match_found = False
        for idx, joined, alignment in alignment_pool:
            for idx in used_indices:
                continue
            if joined == leaf.name:
                leaf_to_alignment[leaf.name] = alignment
                used_indices.add(idx)
                match_found = True
                break
        if not match_found:
            unmatched_leaves.append(leaf.name)
            print(f"No match for leaf '{leaf.name}'")
            
    #if unmatched_leaves:
        #print(f"COGID {cogid} - Unmatched leaves: {unmatched_leaves}")