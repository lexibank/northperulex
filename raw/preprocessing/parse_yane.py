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
    "person (humano)": "PERSON",
    "tooth (front)": "TOOTH",
    "feather (large)": "FEATHER",
    "fruit (berry)": "BERRY",
    "woods (forest)": "FOREST",
    "rope (cord)": "ROPE",
    "thou (you)": "THOU",
    "ye (you all)": "YOU",
    "who (interrog)": "WHO",
    "what (interrog.)": "WHAT",
    "fall (drop)": "FALL",
    "lie (be lying down)": "LIE (REST)",
    "fly (verb)": "FLY (MOVE THROUGH AIR)",
    "turn (intr. v.)": "TURN AROUND",
    "smell (tr. v.)": "SMELL (PERCEIVE)",
    "fear (verb)": "FEAR (BE AFRAID)",
    "count (verb)": "COUNT",
    "spit (verb)": "SPIT",
    "vomit (verb)": "VOMIT",
    "scracth (itch)": "SCRATCH",
    "burn (tr. v.)": "BURNING",
    "tie (verb)": "TIE",
    "cut (verb)": "CUT",
    "stab (or pierce)": "STAB",
    "warm (hot weather)": "WARM (OF WEATHER)",
    "dry (adj./v.)": "DRY",
    "old (adj)": "OLD",
    "where (interrog.)": "WHERE",
    "when (interrog)": "WHEN",
    "how (interrog)": "HOW",
    "with (accompaniment)": "WITH"
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
                        row[4],
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
                    row[4],
                    "",
                    yane_gloss
                ])
            else:
                unmatched_glosses.append(row[1])
                print(f"No match found for gloss: {row[1]}")

with open('../prepared_data/Yanesha.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(filtered_data)
