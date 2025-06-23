import os
from pylotree import Tree

# Load trees
tree_dir = 'trees'
tree_files = [f for f in os.listdir(tree_dir) if f.endswith('.nwk')]

trees = {}
for file in tree_files:
    filepath = os.path.join(tree_dir, file)
    cogid = os.path.splitext(file)[0].split('cogid', 1)[1]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        nwk_str = f.read().strip()
        
    tree = Tree(nwk_str)
    
    for node in tree:
        if not node.descendants:
            if '_' in node.name:
                node.name = node.name.split('_', 1)[1]
    

    trees[cogid] = tree

    