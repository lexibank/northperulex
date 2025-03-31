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
        forms = [entry['Form A'] for entry in entries]
        forms = list(dict.fromkeys(forms))
        writer.writerow([''] + forms)
        
        for i in range(len(forms)):
            row = [forms[i]]
            for j in range(len(forms)):
                form_i = forms[i]
                form_j = forms[j]
                
                # If the forms are identical, set distance to 0.
                # This needs to be change later
                if form_i == form_j:
                    distance = 0.0
                else:
                    form_i_entries = [entry for entry in entries if entry['Form A'] == form_i]
                    form_j_entries = [entry for entry in entries if entry['Form A'] == form_j]
                    
                    distances = [
                        float(entry_i['Combined Distance'])
                        for entry_i in form_i_entries
                        for entry_j in form_j_entries
                        if entry_i['Doculect B'] == entry_j['Doculect A'] or
                           entry_i['Doculect A'] == entry_j['Doculect B']
                    ]
                    
                    if distances:
                        distance = sum(distances) / len(distances)
                    else:
                        distance = 1  # No distance data, set max distance
                
                row.append(round(distance, 4))
            writer.writerow(row)
        writer.writerow([])