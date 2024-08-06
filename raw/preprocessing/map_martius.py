"""
Mapping of latin concepts from Martius to Concepticon.
"""
import csv
from collections import defaultdict
from cldfcatalog import Config
from csvw.dsv import UnicodeDictReader

repos = Config.from_file().get_clone('concepticon')
paths = {p.stem.split('-')[1]: p for p in repos.joinpath(
    'mappings').glob('map-*.tsv')}
mappings = {}

for language, path in paths.items():
    mappings[language] = defaultdict(set)

data = []

# Load manually digitized data
with open("Martius.tsv", mode='r', encoding="utf8") as f:
    wl = csv.reader(f, delimiter="\t")
    next(wl)
    for line in wl:
        if len(line) > 1:
            data.append([line[0], line[1], line[2]])
        else:
            print("Possibly erroneous entry:", line)
            

PATH = "cldf-data/concepticon-data/mappings/map-la.tsv"

with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        gloss = concept['GLOSS'].split('///')[1]
        mappings['la'][gloss].add((concept['ID'], int(concept['PRIORITY'])))

la_data = defaultdict(list)

concept_dic = {}
with open(
    'cldf-data/concepticon-data/concepticondata/concepticon.tsv', mode='r', encoding="utf8"
    ) as file:
    concepticon = csv.reader(file, delimiter="\t")
    for concept in concepticon:
        concept_dic[concept[0]] = concept[1]


# print(mappings)
for i, entry in enumerate(data):
    if entry[1] in mappings['la']:
        best_match, priority = sorted(
            mappings['la'][entry[1]],
            key=lambda x: x[1])[0]

        la_data[best_match] += [[
            str(i+1),
            entry[1],
            best_match,
            concept_dic[best_match],
            priority,
            ]]

    else:
        la_data[entry[1]] = [[
            str(i+1),
            entry[1],
            "",
            "",
            ""
        ]]
        
# Print unmapped entries
print("Unmapped entries:")
for entry in data:
    if entry[1] not in mappings['la']:
        print(f"Doculect: {entry[0]}, Form: {entry[1]}, Notes: Not Mapped")


with open('Martius_mapped.tsv', 'w', encoding="utf8") as f_out:
    f_out.write('ID\tWORD\tCONCEPTICON_ID\tCONCEPTICON_GLOSS\tMATCH\n')
    for key, lines in la_data.items():
        best_line = sorted(lines, key=lambda x: x[-1])[0]
        best_line[-1] = str(best_line[-1])
        f_out.write('\t'.join(best_line)+'\n')
