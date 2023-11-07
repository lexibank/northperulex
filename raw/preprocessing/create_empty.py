import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

langs = defaultdict()
concepts = defaultdict()
visited = []

with open('../../etc/languages.tsv', mode='r', encoding="utf8") as file:
    data = csv.reader(file, delimiter="\t")
    headers = next(data)
    for lines in data:
        if lines[4] == str(0):
            langs[lines[2]] = lines[0]

BASE = "../../../../cldf_resources/concepticon-data/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"


with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']

for lang in langs:
    doculect_data = [[
        "Doculect", "Concept", "Form"
    ]]

    output_file = "empty/" + langs[lang] + ".tsv"
    for item in concepts:
        doculect_data.append([
            langs[lang],
            concepts[item],
            ""
        ])
    with open(output_file, 'w', encoding="utf8", newline='') as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(doculect_data)
