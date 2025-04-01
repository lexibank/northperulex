"""
This script generates distance matrices from the pairwise distances
"""

import csv

# Load data from the input file
data = []
with open("pairwise_distances.tsv", 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        data.append(row)

# Group data by cogid
grouped_data = {}
for row in data:
    cogid = row['Cogid']
    if cogid not in grouped_data:
        grouped_data[cogid] = []
    grouped_data[cogid].append(row)

# Write distance matrices for each Cogid
with open("distance_matrix.tsv", 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    
    for cogid, entries in grouped_data.items():
        writer.writerow([f"Cogid: {cogid}"])
        forms = list({(entry['Doculect A'], entry['Form A']) for entry in entries} |
                     {(entry['Doculect B'], entry['Form B']) for entry in entries})
        
        matrix = {form: {f: "" for f in forms} for form in forms}
        
        for entry in entries:
            form_a = (entry['Doculect A'], entry['Form A'])
            form_b = (entry['Doculect B'], entry['Form B'])
            distance = float(entry['Combined Distance'])
            
            matrix[form_a][form_b] = distance
            matrix[form_b][form_a] = distance
            
        for form in forms:
            matrix[form][form] = 0
            
        header = [""] + [f"{lang}: {form}" for lang, form in forms]
        writer.writerow(header)
        
        for form in forms:
            writer.writerow([f"{form[0]}: {form[1]}"] + [matrix[form][f] for f in forms])
            
        writer.writerow([])