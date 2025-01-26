import csv


# Load data from the input file
data = []
with open("borrowings.tsv", 'r', encoding='utf-8') as file:
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

# Step 3: Write distance matrices for each Cogid
with open("distance_matrix.tsv", 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    
    for cogid, entries in grouped_data.items():
        writer.writerow([f"Cogid: {cogid}"])
        unique_forms = list(set(entry['Form'] for entry in entries))
        writer.writerow([''] + unique_forms)
        
        for i in range(len(unique_forms)):
            row = [unique_forms[i]]
            for j in range(len(unique_forms)):
                form_i = unique_forms[i]
                form_j = unique_forms[j]
                
                if form_i == form_j:  # If the forms are identical, set distance to 0
                    distance = 0.0
                else:
                    form_i_entries = [entry for entry in entries if entry['Form'] == form_i]
                    form_j_entries = [entry for entry in entries if entry['Form'] == form_j]
                    
                    similarities = [
                        float(entry_i['Combined Similarity'])
                        for entry_i in form_i_entries
                        for entry_j in form_j_entries
                        if entry_i['Cogid'] == entry_j['Cogid']
                    ]
                    
                    if similarities:
                        avg_similarity = sum(similarities) / len(similarities)
                        distance = 1 - avg_similarity
                    else:
                        distance = 1  # No similarity data, set max distance
                
                row.append(round(distance, 4))
            writer.writerow(row)
        writer.writerow([])
        
print(f'Distance matrices saved to "distance_matrix.tsv"')
