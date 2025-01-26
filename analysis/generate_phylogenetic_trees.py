import os
from lingpy.convert.strings import multistate2nex

output_directory = 'trees'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

cogid_count = 0

# Load data
with open("distance_matrix.tsv", mode='r') as file:
    lines = file.readlines()
    
cognate_sets = []
matrix = []
labels = []
current_cognate_id = None

for line in lines:
    line = line.strip()
    
    if line.startswith('Cogid:'):
        cogid_count += 1
        if matrix:
            cognate_sets.append((current_cognate_id, labels, matrix))
            matrix = []
            labels = []
            
        current_cognate_id = line.split(':')[1].strip()
    
    elif line and not line.startswith('=') and not labels:
        labels = line.split('\t')[1:]
        labels = ['_'.join(label.split()) for label in labels]  # This is for multi-word labels
        #print(labels)
    
    elif line and line[0] != '=':
        parts = line.split('\t')
        parts = ['_'.join(part.split()) for part in parts]
        #print(parts)
        
        distances = []
        for val in parts[1:]:
            try:
                distances.append(float(val))
            except ValueError:
                distances.append(0.0)
        matrix.append(distances)
        
if matrix:
    cognate_sets.append((current_cognate_id, labels, matrix))

saved_trees = 0
skipped_trees = 0

# Build phylogenetic tree
for cognate_id, labels, matrix in cognate_sets:
    if not labels or not matrix:
        #print(f"Skipping Cognate Set {cognate_id} due to missing data.")
        skipped_trees += 1
        continue  # Skip this cognate set if no labels or matrix data
        
    matrix = [[str(cell) for cell in row] for row in matrix]
    
    output_filename = os.path.join(output_directory, f'phylogenetic_tree_{cognate_id}.nwk')
   
   # Convert to NEXUS format
    multistate2nex(labels, matrix, filename=output_filename, missing='?')
        
    #print(f"Saved tree for Cognate Set {cognate_id} to {output_filename}")
    saved_trees += 1
    
print(f"Total Cognate Sets Processed: {len(cognate_sets)}")
print(f"Total Trees Saved: {saved_trees}")
print(f"Total Trees Skipped: {skipped_trees}")
print(f"Total number of lines containing 'Cogid:': {cogid_count}")