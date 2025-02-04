import csv

# Load data
with open("np_edictor.tsv", mode="r", encoding='utf-8') as f:
    data = csv.reader(f, delimiter='\t')
    rows = list(data)[3:]
    rows = [row for row in rows if not row[0].startswith('#')]
    header = rows[0]
    rows = rows[1:]
    doculects = []
    for row in rows:
        doculect = row[1]
        if doculect not in doculects:
            doculects.append(doculect)
    
    cognate_sets = {}
    
    # Process each row for presence/absence
    for row in rows[0:]:
        cogid = row[8]
        doculect = row[1]
        
        if cogid not in cognate_sets:
            cognate_sets[cogid] = {d: '0' for d in doculects}
        
        cognate_sets[cogid][doculect] = '1'
        
# Output file
with open("presence_absence_matrix.tsv", mode='w', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['COGNATE_SET'] + sorted(doculects))
    for cogid, doculect_data in cognate_sets.items():
        row = [cogid] + [doculect_data[d] for d in sorted(doculects)]
        writer.writerow(row)
    

