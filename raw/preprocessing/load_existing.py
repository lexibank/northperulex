import csv
from pathlib import Path
from collections import defaultdict
from csvw.dsv import UnicodeDictReader
from lingpy import Wordlist

langs = defaultdict()
concepts = defaultdict()
output = [["Doculect", "Concept", "Form"]]

visited = []
with open('../../etc/languages.tsv', mode='r', encoding="utf8") as file:
    data = csv.reader(file, delimiter="\t")
    for lines in data:
        langs[lines[0]] = lines[4]

BASE = "cldf-data/concepticon-data/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"


with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']

wl = Wordlist.from_cldf(
    Path("cldf-data/seifartecheverriboran", "cldf", "cldf-metadata.json").as_posix(),
    columns=(
        "form",
        "segments",
        "concept_name",
        "concept_concepticon_id",
        "concept_concepticon_gloss",
        "language_glottocode"),
    namespace=(
        ("language_glottocode", "doculect"),
        ("concept_name", "concept_name"),
        ("concept_concepticon_gloss", "concept"),
        ("concept_concepticon_id", "concepticon_id"),
        )
)

for idx in wl:
    if wl[idx, "concepticon_id"] in concepts:
        output.append([
            wl[idx, "doculect"],
            wl[idx, "concept"],
            "".join(wl[idx, "segments"])
        ])


wl = Wordlist.from_cldf(
    Path("cldf-data/lexibank-analysed", "cldf", "wordlist-metadata.json").as_posix(),
    columns=(
        "form",
        "segments",
        "concept_name",
        "concept_concepticon_id",
        "concept_concepticon_gloss",
        "language_glottocode"),
    namespace=(
        ("language_glottocode", "doculect"),
        ("concept_name", "concept_name"),
        ("concept_concepticon_gloss", "concept"),
        ("concept_concepticon_id", "concepticon_id"),
        )
)

for idx in wl:
    if langs[wl[idx, "doculect"]] == 1 and wl[idx, "doculect"] not in visited:
        if wl[idx, "concepticon_id"] in concepts:
            output.append([
                wl[idx, "doculect"],
                wl[idx, "concept"],
                "".join(wl[idx, "segments"])
            ])

wl = Wordlist.from_cldf(
    Path("cldf-data/idssegmented", "cldf", "cldf-metadata.json").as_posix(),
    columns=(
        "form",
        "segments",
        "concept_name",
        "concept_concepticon_id",
        "concept_concepticon_gloss",
        "language_glottocode",
        "language_family"),
    namespace=(
        ("language_glottocode", "doculect"),
        ("language_family", "family"),
        ("concept_name", "concept_name"),
        ("concept_concepticon_gloss", "concept"),
        ("concept_concepticon_id", "concepticon_id"),
        )
)

for idx in wl:
    if langs[wl[idx, "doculect"]] == 1 and wl[idx, "doculect"] not in visited:
        if wl[idx, "concepticon_id"] in concepts:
            output.append([
                wl[idx, "doculect"],
                wl[idx, "concept"],
                "".join(wl[idx, "segments"])
            ])

with open("imported/loaded_data.csv", 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)
