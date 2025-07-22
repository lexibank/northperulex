from lingpy import Wordlist, LexStat, Alignments
import re
from lingpy.compare.partial import Partial
from lingpy.sequence.sound_classes import tokens2class
from lingpy.compare.sanity import mutual_coverage_subset

def clean_slash(x):
	"""Cleans slash annotation from EDICTOR."""
	cleaned = []
	for segment in x:
		if "/" in segment:
			after_slash = re.split("/", segment)[1]
			cleaned.append(after_slash)
		else:
			cleaned.append(segment)

	return cleaned

# Data preprocessing
cols = [
	'concept_id', 'concept_name', 'language_id', 'language_name', 'value', 'form', 'segments',
	'glottocode', 'concept_concepticon_id', 'comment', 'language_family', 'language_subgroup'
]

# Load dataset
wl = Wordlist.from_cldf(
	'../cldf/cldf-metadata.json',
	columns=cols,
	namespace=(
		("language_id", "doculect"),
		("language_family", "family"),
		("language_subgroup", "subgroup"),
		("concept_name", "concept"),
		("segments", "tokens"),
		("cognacy", "cogid")
	))

# Delete unnecessary tokens with clean_slash
for idx in wl:
	wl[idx, "tokens"] = [x.split("/")[1] if "/" in x else x for x in wl[idx, "tokens"]]

# Check mutual coverage in the language sample and select subset of languages
number_of_languages, pairs = mutual_coverage_subset(wl, 100)
for number_of_items, languages in pairs:
	print(number_of_items, ', '.join(languages))

selected_ls = set().union(*(langs for _, langs in pairs))

selected_ls.discard("Proto-Bora-Muinane")

D = {0: [c for c in wl.columns]}
for idx in wl:
	if (
			wl[idx, "doculect"] in selected_ls
	):
		D[idx] = [wl[idx, c] for c in D[0]]

wl_filtered = Wordlist(D)

#wl_filtered.output(
#	"tsv",
#	filename="npl-filtered"
#)

# Run AutoCogid
lex = LexStat(wl_filtered)
lex.get_scorer(runs=10000)
lex.cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="cogid")

# Get morpheme segmentation
parcog = Partial(lex, segments='tokens')
parcog.partial_cluster(threshold=0.55, method="lexstat", ref="cogids")

# Align data
alms = Alignments(parcog, ref="cogids", transcription="tokens")
alms.align(ref="cogids")
alms.add_entries("morphemes","tokens", lambda x: " ".join([y for y in x]), override=True)
alms.add_entries("alignment", "tokens", lambda x: " ".join([y for y in x]), override=True)
alms.add_entries("structure", "tokens", lambda x: tokens2class(x, "cv"))

alms.output("tsv", filename="npl")