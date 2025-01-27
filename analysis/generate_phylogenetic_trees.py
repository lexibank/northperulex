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
        labels = line.split('\t')[0:]
        labels = ['_'.join(label.split()) for label in labels]  # This is for multi-word labels
        print(labels)
    
    elif line and line[0] != '=':
        parts = line.split('\t')
        parts = ['_'.join(part.split()) for part in parts]
        #print(parts)
        
        taxon = parts[0]
        if taxon not in labels:
            labels.append(taxon)
        
        try:
            distances = [float(val) for val in parts[1:]]
        except ValueError:
            distances = [0.0 for _ in parts[1:]]
        matrix.append(distances)
        #print(distances)
        
if matrix and labels:
    cognate_sets.append((current_cognate_id, labels, matrix))
    #print(matrix)

saved_trees = 0
skipped_trees = 0

# Build phylogenetic tree
for cognate_id, labels, matrix in cognate_sets:
    if not labels or not matrix:
        skipped_trees += 1
        continue
        
    matrix = [' '.join(map(str, row)) for row in matrix]
    
    output_filename = os.path.join(output_directory, f'tree_{cognate_id}.nex')
   
   # Convert to NEXUS format
    multistate2nex(labels, matrix, filename=output_filename, missing='?')
        
    #print(f"Saved tree for Cognate Set {cognate_id} to {output_filename}")
    saved_trees += 1
    
# Write simple summary to a markdown file
with open(os.path.join(output_directory, 'summary.md'), 'w') as md_file:
    md_file.write("## Summary\n\n")
    md_file.write(f"- **Total Cognate Sets Processed:** {len(cognate_sets)}\n\n")
    md_file.write(f"- **Total Trees Saved:** {saved_trees}\n")
    md_file.write(f"- **Total Trees Skipped:** {skipped_trees}\n\n")
    md_file.write(f"- **Total number of lines containing 'Cogid:':** {cogid_count}\n")
