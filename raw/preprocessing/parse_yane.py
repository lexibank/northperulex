import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

data = []
mappings = defaultdict(list)

PATH = "cldf-data/concepticon-data/mappings/map-en.tsv"
with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        gloss = concept['GLOSS'].split('///')[1]
        mappings[gloss].append((concept['ID'], int(concept['PRIORITY'])))

# Load concept list
BASE = "cldf-data/concepticon-data/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"

concepts = {}
with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']

# Iterate through data and filter entries

filtered_data = [[
    "Doculect", "Concept", "Form", "Note", "Gloss"
]]
unmatched_glosses = []
gloss_mapping = {
    "person (humano)": "",
}

with open('Yanesha.csv', mode='r', encoding="utf-8") as f:
    data = csv.reader(f, delimiter="\t")
    for row in data:
        yane_gloss = row[1].strip()
        mapped = 0
        
        if yane_gloss in mappings:
            for mapping in mappings[yane_gloss]:
                concept_id, priority = mapping
                if concept_id in concepts:
                    filtered_data.append([
                        "Yanesha",
                        concepts[concept_id],
                        row[3],
                        "",
                        yane_gloss
                    ])
                    mapped += 1

        if mapped == 0:
            concepticon_gloss = gloss_mapping.get(yane_gloss)
            if concepticon_gloss:
                filtered_data.append([
                    "Wampis",
                    concepticon_gloss,
                    row[3],
                    "",
                    yane_gloss
                ])
            else:
                unmatched_glosses.append(row[1])
                print(f"No match found for gloss: {row[1]}")

with open('../prepared_data/Yanesha.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(filtered_data)
