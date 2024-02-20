import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

data = []
concepts = defaultdict()

# Load concept list
BASE = "/Users/cb17/Library/Application Support/cldf/concepticon/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"

with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']
        #print(line)
		
# Iterate through data and filter entries
filtered_data = []

with open('Urarina.csv', mode='r', encoding="utf-8") as file:
    data = csv.reader(file, delimiter="\t")
    for row in data:
        if row[7] in concepts:
            filtered_data.append(row)
            
for entry in filtered_data:
    print(entry)