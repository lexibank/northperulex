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
        langs[lines[2]] = lines[0]

LIST = "cldf-data/concepticon-data/concepticondata/conceptlists/Tadmor-2009-100.tsv"


with UnicodeDictReader(LIST, delimiter='\t') as reader:
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
