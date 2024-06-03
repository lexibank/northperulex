
import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader
from cldfcatalog import Config

repos = Config.from_file().get_clone('concepticon')
paths = {p.stem.split('-')[1]: p for p in repos.joinpath('mappings').glob('map-*.tsv')}
mappings = {}

for language, path in paths.items():
    mappings[language] = defaultdict(set)

BASE = 'cldf-data/concepticon-data/'
LIST = BASE + 'concepticondata/conceptlists/Tadmor-2009-100.tsv'
PATH = BASE + 'mappings/map-pt.tsv'

with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        mappings['pt'][concept['ID']] = concept['GLOSS'].split('///')[1]

pt_data = [['CONCEPTICON_ID', 'CONCEPTICON_GLOSS', 'PORTUGUESE', 'FORM']]

with UnicodeDictReader(LIST, delimiter='\t') as reader:
    for line in reader:
        if line['CONCEPTICON_ID'] in mappings['pt']:
            pt_data.append([
                line['CONCEPTICON_ID'],
                line['CONCEPTICON_GLOSS'],
                mappings['pt'][line['CONCEPTICON_ID']],
                ''])
        else:
            pt_data.append([
                line['CONCEPTICON_ID'],
                line['CONCEPTICON_GLOSS'],
                '',
                ''])

with open('pt_data.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(pt_data)
