from lingpy import Wordlist, LexStat, Alignments
import re
from lingpy.compare.partial import Partial
from lingrex.copar import CoPaR
from lingpy.sequence.sound_classes import tokens2class


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

# Deleting unnecessary tokens with clean_slash
for idx in wl:
	wl[idx, "tokens"] = [x.split("/")[1] if "/" in x else x for x in wl[idx, "tokens"]]
	
# Run AutoCogid
lex = LexStat(wl)
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

# Infer sound correspondances
cop = CoPaR(alms, transcription="form", ref="cogid")
cop.get_sites()
cop.cluster_sites()
cop.sites_to_pattern()
#cop.add_patterns()
# Write patterns
#cop.write_patterns('np_patterns.tsv')

# Run AutoCogid
cop_wl = LexStat(cop)
cop_wl.get_scorer(runs=10000)
cop_wl.cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="cogid")

cop_wl.output('tsv', filename='npl_copped', ignore='all')