
import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader
from cldfcatalog import Config

repos = Config.from_file().get_clone('concepticon')
paths = {p.stem.split('-')[1]: p for p in repos.joinpath(
    'mappings').glob('map-*.tsv')}
mappings = {}

for language, path in paths.items():
    mappings[language] = defaultdict(set)

BASE = 'cldf-data/concepticon-data/'
SWAD_200 = BASE + "concepticondata/conceptlists/Swadesh-1952-200.tsv"
PATH = BASE + "mappings/map-es.tsv"

with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        gloss = concept['GLOSS'].split('///')[1]
        mappings['es'][concept['ID']] = gloss

es_data = [['CONCEPTICON_ID', 'CONCEPTICON_GLOSS', 'SPANISH', 'FORM']]
with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        if line['CONCEPTICON_ID'] in mappings['es']:
            es_data.append([
                line['CONCEPTICON_ID'],
                line['CONCEPTICON_GLOSS'],
                mappings['es'][line['CONCEPTICON_ID']],
                ''])
        else:
            es_data.append([
                line['CONCEPTICON_ID'],
                line['CONCEPTICON_GLOSS'],
                '',
                ''])

with open('concepts_data.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(es_data)
