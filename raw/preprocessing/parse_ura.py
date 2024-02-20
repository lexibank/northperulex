import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

data = []
concepts = defaultdict()

with open('Urarina.csv', mode='r', encoding="utf-8") as file:
    data = csv.reader(file, delimiter="\t")
    headers = next(data)
    for rows in data:
        print(data)

# Load concept list
BASE = "/Users/cb17/Library/Application Support/cldf/concepticon/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"

with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']
		
# Iterate through data and filter entries

for row in rows:
    filtered_data = []
    for item in concepts:
        # Here is where it breaks. I believe the code is not being able to access the 7th column for each of the roads and
        # therefore not being able to match it to the concepts dict
        if row[7] in concepts:
            filtered_data.append([
                rows[row],
                concepts[item]
            ])
            
for entry in filtered_data:
    print(entry)