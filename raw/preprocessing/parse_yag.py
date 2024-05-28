import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

spanish_mappings = defaultdict(list)

PATH = "cldf-data/concepticon-data/mappings/map-es.tsv"
with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        gloss_parts = concept['GLOSS'].split('///')
        first_part = gloss_parts[0]
        second_part = gloss_parts[1]
        spanish_mappings[second_part].append((concept['ID'], int(concept['PRIORITY']), first_part))

# Load concept list
BASE = "cldf-data/concepticon-data/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"

concepts = {}
with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']
		
# Iterate through data and filter entries

filtered_data = [[
        "Doculect", "Concept", "Form", "Note", "Spanish"
    ]]

with open("Yagua.tsv", mode='r', encoding="utf-8") as file:
    lines = file.readlines()
    
lines = [line.strip() for line in lines[3:] if line.strip()]

word_pairs = []

for i in range(0, len(lines), 2):
    yagua_words = lines[i].split()[1:]  # Extract Yagua words from the line
    spanish_words = lines[i + 1].split()[1:]  # Extract Spanish words from the next line
    spanish_words = [word.split('_')[-1] if '_' in word else word for word in spanish_words]
    pairs = [(yagua, spanish, first_part) for yagua, spanish, first_part in zip(yagua_words, spanish_words, [
        spanish_mappings.get(spanish, [(None, None, None)])[0][2] for spanish in spanish_words]) if
             spanish in spanish_mappings]
    word_pairs.extend(pairs)  # Extend the list with pairs
    
for yagua, spanish, first_part in word_pairs:
    filtered_data.append(["Yagua", first_part, yagua, "", spanish])

with open('../prepared_data/Yagua.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(filtered_data)