import csv
import os
import math
from ete3 import Tree

output_dir = 'recons_trees'
os.makedirs(output_dir, exist_ok=True)

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
        
def get_states(cogid_data):
    states = set()
    for alignments in cogid_data.values():
        for _, alignment in alignments:
            for segment in alignment:
                if segment != '+':
                    states.add(segment)
    return sorted(states)

# Sankoff algorithm
def sankoff_parsimony(tree, leaf_to_alignment, states):
    """
    This is the function for ancestral state reconstruction that
    implements Sankoff's maximum parsimony algorithm.
    The function penalizes insertion twice as much as deletion.
    """
    reconstructions = []
    
    # Assign costs to leaves
    def unit_cost(i, j):
        if i == j:
            return 0
        elif i == '-' and j != '-':
            return 2 # Gain is more costly
        elif i != '-' and j == '-':
            return 1 # Lost is less costly
        else:
            return 1
    
    alignment_length = len(next(iter(leaf_to_alignment.values())))
    
    # Run algorithm position by position
    for pos in range(alignment_length):
        # The next line is because the alignments are not perfect yet
        # Make sure all alignments have this position
        if any(len(alignment) <= pos for alignment in leaf_to_alignment.values()):
            continue
        
        position_states = {
            name: alignment[pos]
            for name, alignment in leaf_to_alignment.items()
            #if len(alignment) > pos
        }
        
        if len(position_states) < len(leaf_to_alignment):
            continue
        
        costs_per_node = {}
        
        # Compute costs bottom-up
        for node in tree.traverse("postorder"):
            costs = {}
            if node.is_leaf():
                observed = position_states.get(node.name, None)
                for s in states:
                    costs[s] = 0 if s == observed else math.inf
            else:
                c1_costs = costs_per_node[node.children[0]]
                c2_costs = costs_per_node[node.children[1]]
                for s in states:
                    c1 = min(unit_cost(s, j) + c1_costs[j] for j in states)
                    c2 = min(unit_cost(s, j) + c2_costs[j] for j in states)
                    costs[s] = c1 + c2
            costs_per_node[node] = costs
    
    
        reconstruction = {}
        
        def backtrack(node, parent_state=None):
            if parent_state is None:
                state = min(costs_per_node[node], key=costs_per_node[node].get)
            else:
                possible = costs_per_node[node]
                state = min(possible, key=lambda s: unit_cost(parent_state, s) + possible[s])
            reconstruction[node.name] = state
            for child in node.children:
                backtrack(child, state)
            
        backtrack(tree.get_tree_root())
        reconstructions.append(reconstruction)
        
    return reconstructions

# Run everything
all_states = get_states(cogid_data)

for cogid, tree in trees.items():
    if cogid not in cogid_data:
        continue
        
    # Match alignments to leaves
    leaf_to_alignment = {}
    leaves = [leaf.name for leaf in tree.iter_leaves()]
    alignment_pool = [(i, ''.join(aln), aln) for i, (_, aln) in enumerate(cogid_data[cogid])]
    used_indices = set()
    for leaf in tree.iter_leaves():
        for idx, joined, alignment in alignment_pool:
            for idx in used_indices:
                continue
            if joined == leaf.name:
                leaf_to_alignment[leaf.name] = alignment
                used_indices.add(idx)
                break
                
    if len(leaf_to_alignment) != len(leaves):
        continue
        
    reconstructions = sankoff_parsimony(tree, leaf_to_alignment, all_states)
    
    root = tree.get_tree_root()
    reconstructed_root_form = ''.join([recon[root.name] for recon in reconstructions])
    print(f"COGID {cogid} - Reconstructed root: {reconstructed_root_form}")
    
    # Assign reconstructions to internal nodes
    for i, recon in enumerate(reconstructions):
        for node in tree.traverse("postorder"):
            if not node.is_leaf():
                if not hasattr(node, "reconstructed"):
                    node.reconstructed = []
                node.reconstructed.append(recon.get(node.name, '-'))
                
    for node in tree.traverse("postorder"):
        if not node.is_leaf() and hasattr(node, "reconstructed"):
            node.name = ''.join(node.reconstructed)
            
    # Export reconstructed trees
    tree_file_path = os.path.join(output_dir, f"reconstructed_cogid{cogid}.nwk")
    tree.write(outfile=tree_file_path, format=1)