import csv
from pathlib import Path
from collections import defaultdict
from csvw.dsv import UnicodeDictReader
from lingpy import Wordlist

langs = defaultdict()
concepts = defaultdict()
output = []
visited = []
with open('../../etc/languages.tsv', mode='r', encoding="utf8") as file:
    data = csv.reader(file, delimiter="\t")
    for lines in data:
        langs[lines[2]] = lines[0]

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
    if wl[idx, "doculect"] in langs:
        if wl[idx, "concepticon_id"] in concepts:
            output.append([
                wl[idx, "doculect"],
                wl[idx, "concept"],
                wl[idx, "segments"]
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
    if wl[idx, "doculect"] in langs and wl[idx, "doculect"] not in visited:
        if wl[idx, "concepticon_id"] in concepts:
            output.append([
                wl[idx, "doculect"],
                wl[idx, "concept"],
                wl[idx, "segments"]
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
    if wl[idx, "doculect"] in langs and wl[idx, "doculect"] not in visited:
        if wl[idx, "concepticon_id"] in concepts:
            output.append([
                wl[idx, "doculect"],
                wl[idx, "concept"],
                wl[idx, "segments"]
            ])

with open("imported/loaded_data.csv", 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)

syns = defaultdict()
lang_count = defaultdict()
covered = []
for item in wl:
    checkup = [
        wl[item, "doculect"],
        wl[item, "concept"]
        ]
    if checkup[0] not in syns:
        syns[checkup[0]] = 0
        lang_count[checkup[0]] = 0
    if checkup in covered:
        syns[checkup[0]] = syns[checkup[0]] + 1
    else:
        lang_count[checkup[0]] = lang_count[checkup[0]] + 1
        covered.append(checkup)

covs = 0
syno = 0
for x in syns:
    coverage = round((lang_count[x] / len(concepts)), 2)
    covs += coverage
    synonyms = round(((syns[x]+lang_count[x]) / lang_count[x]), 2)
    syno += synonyms
    print("---")
    print("Language:", x)
    print("Total coverage", coverage)
    print("Synonyms:", synonyms)
