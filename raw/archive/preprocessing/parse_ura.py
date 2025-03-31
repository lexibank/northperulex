import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

data = []
concepts = defaultdict()

# Load concept list
BASE = "cldf-data/concepticon-data/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"

with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']
		
# Iterate through data and filter entries

filtered_data = [[
        "Doculect", "Concept", "Form", "Note"
    ]]

with open('Urarina.csv', mode='r', encoding="utf-8") as file:
    data = csv.reader(file, delimiter=",")
    headers = next(data)
    for row in data:
        if row[7] in concepts:
            filtered_data.append([
                "Urarina",
                row[8],
                row[2],
                ""
            ])

with open('../prepared_data/Urarina.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(filtered_data)