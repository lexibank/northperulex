from collections import defaultdict
from pathlib import Path
from lingpy import Wordlist
from lingpy.compare.sanity import average_coverage, mutual_coverage
from tabulate import tabulate

path = Path(".")
wl = Wordlist.from_cldf(
	"../cldf/cldf-metadata.json",
	columns=(
		"concept_id",
		"language_id",
		"concept_name",
		"language_name",
		"value",
		"segments",
		"form",
		"glottocode",
		"concept_concepticon_ide",
		"source",
		"language_subgroup"
	),
	namespace=(
		("language_id", "doculect"),
		("language_subgroup", "subgroup"),
		("concept_name", "concept"),
		("segments", "tokens"),
		("cognacy", "cogid"),
		("source", "source")
	)
)

lang_count = defaultdict(int)
total_concepts = len(set(wl.get_list("concept", flat=True)))

for item in wl:
	lang = wl[item, "doculect"]
	lang_count[lang] = lang_count[lang] + 1
	
table_data = []
covs_total = 0

for lang in sorted(lang_count.keys()):
	# Calculate coverage percentage
	coverage_pctg = round((lang_count[lang] / total_concepts) * 100, 1)
	covs_total += coverage_pctg
	
	indices = wl.get_list(col=lang, flat=True)
	if indices:
		idx = indices[0]
		lang_name = wl[idx, "language_name"]
		glottocode = wl[idx, "glottocode"]
		subgroup = wl[idx, "subgroup"]
		source = wl[idx, "source"]
		
		table_data.append([
			lang_name,
			glottocode,
			subgroup,
			source,
			f"{lang_count[lang]} ({coverage_pctg}%)"
		])
		
table = tabulate(
	table_data,
	headers=[
		"Language",
		"Glottocode",
		"Language Family",
		"Sources",
		"Coverage"
	],
	tablefmt="pipe"
)

print(table)
	