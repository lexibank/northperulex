"""
Filtering the concepts from Tessmann for being part of Swadesh-200 or not.
"""
import csv
from collections import defaultdict
from glob import glob
from csvw.dsv import UnicodeDictReader

concepts = []
concepts_tess = defaultdict()

BASE = 'cldf-data/concepticon-data/'
SWAD_200 = BASE + "concepticondata/conceptlists/Swadesh-1952-200.tsv"

with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts.append([
            line['CONCEPTICON_ID'],
            line['CONCEPTICON_GLOSS']
            ])


with UnicodeDictReader('Tessmann_mapped.tsv', delimiter='\t') as file:
    for line in file:
        concepts_tess[line['WORD']] = [line['CONCEPTICON_ID'], line['CONCEPTICON_GLOSS']]

data = [[
    "Doculect", "Concept", "Form", "Notes"
]]

# Load manually digitized data
datasets = list(sorted(glob("../prepared_data/Tessmann/*.tsv")))

def add_wl(doc):
    """Adds data from languages in folder."""
    name = doc.split("/")[3][:-4]
    with open(doc, mode='r', encoding="utf8") as f:
        wl = csv.reader(f, delimiter="\t")
        next(wl)
        for entry in wl:
            if len(entry) > 1 and concepts_tess[entry[0]] in concepts:
                comment = 'Tessmann: ' + entry[0]
                data.append([name, concepts_tess[entry[0]][1], entry[1], comment])

for lang in datasets:
    add_wl(lang)

with open('../prepared_data/Tessmann_combined.tsv', 'w', encoding="utf8", newline='') as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(data)
