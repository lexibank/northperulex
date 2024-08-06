"""
Filtering the concepts from Martius for being part of Swadesh-200 or not.
"""
import csv
from collections import defaultdict
from glob import glob
from csvw.dsv import UnicodeDictReader

concepts = []
concepts_mart = defaultdict()

BASE = 'cldf-data/concepticon-data/'
SWAD_200 = BASE + "concepticondata/conceptlists/Swadesh-1952-200.tsv"

with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts.append([
            line['CONCEPTICON_ID'],
            line['CONCEPTICON_GLOSS']
            ])


with UnicodeDictReader('Martius_mapped.tsv', delimiter='\t') as file:
    for line in file:
        concepts_mart[line['WORD']] = [line['CONCEPTICON_ID'], line['CONCEPTICON_GLOSS']]

data = [[
    "Doculect", "Concept", "Form", "Notes"
]]


with open("Martius.tsv", mode='r', encoding="utf8") as f:
    wl = csv.reader(f, delimiter="\t")
    next(wl)
    for entry in wl:
        if len(entry) > 1:
            if entry[1] not in concepts_mart:
                print(f"Missing key in concepts_mart: {entry[1]}")
            elif concepts_mart[entry[1]] in concepts:
                comment = 'Martius: ' + entry[1]
                data.append([entry[0], concepts_mart[entry[1]][1], entry[2], comment])
            

with open('../prepared_data/Martius_combined.tsv', 'w', encoding="utf8", newline='') as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(data)
