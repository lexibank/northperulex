import csv
import numpy as np
from collections import defaultdict
import os

os.makedirs('bimatrices', exist_ok=True)

# Load data
data  = []
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
    
# Generating binary matrices
for cogid, forms_alignments in cogid_data.items():
    max_slots = max(len(alignment) for _, alignment in forms_alignments)
    # Empty matrix
    binary_matrix = np.zeros((len(forms_alignments), max_slots), dtype=int)
    # Fill it
    forms = []
    for i, (form, alignment) in enumerate(forms_alignments):
        forms.append(form)
        for j, slot in enumerate(alignment):
            binary_matrix[i, j] = 1 if slot != '-' else 0
            
    # Output file
    output_file = f'bimatrices/binarymatrix_cogid{cogid}.tsv'
    with open(output_file, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        header = ['FORM'] + [f'Slot{j+1}' for j in range(max_slots)]
        writer.writerow(header)
        for i, form in enumerate(forms):
            writer.writerow([form] + list(binary_matrix[i]))