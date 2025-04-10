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
    trees[cogid] = Tree(filepath, format=1)


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
    cogid = row[5]
    alignment = row[23].split()
    form = row[5]
    if cogid not in cogid_data:
        cogid_data[cogid] = []
    cogid_data[cogid].append((form, alignment))

if '2978' in cogid_data:
    for form, alignment in cogid_data['2978']:
        print(f"{form}: {alignment}")

# Extract all characters
def get_characters(cogid_data):
    characters = set()
    for alignments in cogid_data.values():
        for _, alignment in alignments:
            characters.update(alignment)
    return sorted(characters)


# Sankoff algorithm
def sankoff_parsimony(tree, alignment, states):
    state_costs = {}

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

# Run everything
all_states = get_characters(cogid_data)

for cogid, tree in trees.items():
    if cogid not in cogid_data:
        continue
    alignments = cogid_data[cogid]
    form_to_alignment = {form: aln for form, aln in alignments}

    aln_len = len(next(iter(form_to_alignment.values())))

    print(f"\nCOGID: {cogid}")

    for pos in range(aln_len):
        # Alignment for current position
        alignment_at_pos = {
            form: aln[pos] for form, aln in form_to_alignment.items()
        }

        state_costs = sankoff_parsimony(tree, alignment_at_pos, all_states)

        print(f" Position {pos}:")
        for node in [n for n in tree.traverse() if not n.is_leaf()]:
            node_label = node.name or f"Node_{id(node)}"
            min_cost = min(state_costs[node].values())
            best_states = [s for s in all_states if state_costs[node][s] == min_cost]
            print(f"  {node_label}: {best_states}")
