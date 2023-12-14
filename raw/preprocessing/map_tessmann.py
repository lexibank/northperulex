"""
Mapping of german concepts from Tessmann to Concepticon.
"""
import csv
from collections import defaultdict
from glob import glob
from cldfcatalog import Config
from csvw.dsv import UnicodeDictReader

repos = Config.from_file().get_clone('concepticon')
paths = {p.stem.split('-')[1]: p for p in repos.joinpath(
    'mappings').glob('map-*.tsv')}
mappings = {}

for language, path in paths.items():
    mappings[language] = defaultdict(set)

data = [[
    "Doculect", "Concept", "Form"
]]


# Load manually digitized data
datasets = list(sorted(glob("../prepared_data/Tessmann/*.tsv")))

def add_wl(file):
    """Adds data from languages in folder."""
    name = file.split("/")[3][:-4]
    with open(file, mode='r', encoding="utf8") as f:
        wl = csv.reader(f, delimiter="\t")
        next(wl)
        for line in wl:
            if len(line) > 1:
                data.append([
                    name, line[0], line[1]
                    ])
            else:
                print("Wrong entry:", name, line)


for lang in datasets:
    add_wl(lang)

PATH = "cldf-data/concepticon-data/mappings/map-de.tsv"

with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        gloss = concept['GLOSS'].split('///')[1]
        mappings['de'][gloss].add((concept['ID'], int(concept['PRIORITY'])))

de_data = defaultdict(list)


concept_dic = {}
with open(
    'cldf-data/concepticon-data/concepticondata/concepticon.tsv', mode='r', encoding="utf8"
    ) as f:
    concepticon = csv.reader(f, delimiter="\t")
    for concept in concepticon:
        concept_dic[concept[0]] = concept[1]


# print(mappings)
for i, entry in enumerate(data):
    if entry[1] in mappings['de']:
        best_match, priority = sorted(
            mappings['de'][entry[1]],
            key=lambda x: x[1])[0]

        de_data[best_match] += [[
            str(i+1),
            entry[1],
            best_match,
            concept_dic[best_match],
            priority,
            ]]

    else:
        de_data[entry[1]] = [[
            str(i+1),
            entry[1],
            "",
            "",
            ""
        ]]


with open('Tessmann.tsv', 'w', encoding="utf8") as f_out:
    f_out.write('ID\tWORD\tCONCEPTICON_ID\tCONCEPTICON_GLOSS\tMATCH\n')
    for key, lines in de_data.items():
        best_line = sorted(lines, key=lambda x: x[-1])[0]
        best_line[-1] = str(best_line[-1])
        f_out.write('\t'.join(best_line)+'\n')
