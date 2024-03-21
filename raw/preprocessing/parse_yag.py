import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader
import re

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

with open("Yagua.tsv", mode='r', encoding="utf-8") as file:
    lines = file.readlines()
    
lines = [line.strip() for line in lines[3:] if line.strip()]

word_pairs = []

for i in range(0, len(lines), 2):
    yagua_words = lines[i].split()[1:]  # Extract Yagua words from the line
    spanish_words = lines[i + 1].split()[1:]  # Extract Spanish words from the next line
    pairs = list(zip(yagua_words, spanish_words))  # Zip Yagua and Spanish words together
    word_pairs.extend(pairs)  # Extend the list with pairs
    
for pair in word_pairs:
    print(pair)

with open('../prepared_data/Yagua.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(filtered_data)