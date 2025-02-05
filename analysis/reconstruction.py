import csv
import os
from ete3 import Tree
from collections import Counter, defaultdict

# Load trees
tree_dir = 'trees/'
tree_files = [f for f in os.listdir(tree_dir) if f.endswith('.nwk')]

def load_trees(tree_files):
    cogid_tree_mapping = {}
    for file in tree_files:
        cogid = file.split('cogid')[-1].replace('.nwk', '')
        with open(os.path.join(tree_dir, file)) as f:
            tree = Tree(f.read(), format=1)
            cogid_tree_mapping[cogid] = tree
    return cogid_tree_mapping


cogid_tree_mapping = load_trees(tree_files)

# Load alignments
data = []
with open('np_edictor.tsv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    for i, row in enumerate(reader):
        if i < 3 or (len(row) > 0 and row[0].startswith('#')):
            continue
        data.append(row)

# Group by COGID
cogid_data = {}
for row in data[1:]:
    cogid = row[8]
    alignment = row[10].split()
    form = row[5]
    if cogid not in cogid_data:
        cogid_data[cogid] = []
    cogid_data[cogid].append((form, alignment))


def assign_and_compute_states(tree, alignments):
    # Assign initial states (aligned sequences) to leaves
    for leaf in tree.get_leaves():
        for form, alignment in alignments:
            if form == leaf.name:  # Match leaf name with the form
                leaf.state = alignment
                break
        else:
            leaf.state = []
    
    # Compute ancestral state for internal nodes
    def compute_ancestralState(node):
        if node.is_leaf():
            return node.state
        child_states = [compute_ancestralState(child) for child in node.children]
        max_length = max(len(state) for state in child_states)
        padded_states = [state + ['_'] * (max_length - len(state)) for state in child_states]
        
        ancestral_state = []
        for position in range(max_length):
            chars = [state[position] for state in padded_states]
            most_common_char = Counter(chars).most_common(1)[0][0]
            ancestral_state.append(most_common_char)
        
        node.state = ancestral_state
        return ancestral_state
    
    compute_ancestralState(tree)


# Output file
output_file = "frequency_reconstruction.tsv"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("CogID\tNode Type\tReconstructed State\n")
    for cogid, tree in sorted(cogid_tree_mapping.items(), key=lambda x: int(x[0])):
        alignments = cogid_data.get(cogid, [])
        assign_and_compute_states(tree, alignments)
        
        for node in tree.traverse():
            node_type = "Internal Node" if not node.is_leaf() else "Leaf"
            reconstructed_state = " ".join(node.state) if node.state else "N/A"
            f.write(f"{cogid}\t{node_type}\t{reconstructed_state}\n")
        
        
    # Define the parsimony distance (transition cost) between different states
    def parsimony_cost(state1, state2):
        # Simple cost: 0 for identical, 1 for different characters
        return sum(1 for c1, c2 in zip(state1, state2) if c1 != c2)
        
        
    # Compute ancestral state for internal nodes using parsimony
    def compute_withparsimony(node):
        if node.is_leaf():
            return node.state
        child_states = [compute_withparsimony(child) for child in node.children]
            
        # Find the state that minimizes the parsimony cost
        possible_states = []
        all_states = set(state for child in node.children for state in child.state)
            
        for state in all_states:
            total_cost = 0
            for child_state in child_states:
                # Calculate the transition cost to this state for each child
                total_cost += min(parsimony_cost(state, cs) for cs in child_state)
            possible_states.append((state, total_cost))
            
        # Select the state with the minimal cost
        best_state = min(possible_states, key=lambda x: x[1])[0]
        node.state = best_state
        return node.state
        
        
    compute_withparsimony(tree)
    
# Output file
output_file = "parsimony_reconstruction.tsv"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("CogID\tNode Type\tReconstructed State\n")
    for cogid, tree in sorted(cogid_tree_mapping.items(), key=lambda x: int(x[0])):
        alignments = cogid_data.get(cogid, [])
        assign_and_compute_states(tree, alignments)
            
        for node in tree.traverse():
            node_type = "Internal Node" if not node.is_leaf() else "Leaf"
            reconstructed_state = " ".join(node.state) if node.state else "N/A"
            f.write(f"{cogid}\t{node_type}\t{reconstructed_state}\n")