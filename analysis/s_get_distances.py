from lingpy.compare.strings import ldn_swap, bidist2, tridist2
import csv
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
alms.add_entries("morphemes", "tokens", lambda x: " ".join([y for y in x]), override=True)
alms.add_entries("alignment", "tokens", lambda x: " ".join([y for y in x]), override=True)
alms.add_entries("structure", "tokens",
				 lambda x: tokens2class(x, "cv"))

#alms.output("tsv", filename="npl")

# Infer sound correspondances
cop = CoPaR(alms, transcription="form", ref="cogids")
cop.get_sites()
cop.cluster_sites()
cop.sites_to_pattern()
# cop.add_patterns()
# Write patterns
# cop.write_patterns('np_patterns.tsv')

# Run AutoCogid
cop_wl = LexStat(cop)
cop_wl.get_scorer(runs=10000)
cop_wl.cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="cogids")

#cop_wl.output('tsv', filename='npl_copped', ignore='all')

# Collecting necessary data
distances = []
for idx in cop_wl:
	doculect_a = cop_wl[idx, 'doculect']
	form_a = cop_wl[idx, 'tokens']
	family_a = cop_wl[idx, 'family']
	concept = cop_wl[idx, 'concept']
	cluster_id = cop_wl[idx, 'cogid']
	
	for other_idx in cop_wl:
		if other_idx != idx and cop_wl[other_idx, 'cogid'] == cluster_id:
			doculect_b = cop_wl[other_idx, 'doculect']
			family_b = cop_wl[other_idx, 'family']
			
			if doculect_a != doculect_b:
				form_b = cop_wl[other_idx, 'tokens']
				alignment_a = alms[idx]
				alignment_b = alms[other_idx]
				
				# Calculate identity score based on alignment
				aligned_columns = 0
				identical_columns = 0
				if alignment_a and alignment_b:
					for seg1, seg2 in zip(alignment_a, alignment_b):
						aligned_columns += 1
						if seg1 == seg2:
							identical_columns += 1
				identity_score = (identical_columns / aligned_columns) if aligned_columns > 0 else 0
				# Convert identity score into distance
				distance_from_identity = 1 - identity_score
				
				# Calculate Levenshtein distance with swap included
				levenshtein_distance = ldn_swap(form_a, form_b, normalized=True)
				
				# Calculate Bigram and Trigram Distances
				bigram_distance = bidist2(form_a, form_b, normalized=True)
				trigram_distance = tridist2(form_a, form_b, normalized=True)
				
				# Combined Distances
				combined_distance = (
						0.25 * distance_from_identity +
						0.25 * levenshtein_distance +
						0.25 * bigram_distance +
						0.25 * trigram_distance
				)
				
				distances_info = {
					"doculect_a": doculect_a,
					"doculect_b": doculect_b,
					"concept": concept,
					"form_a": form_a,
					"form_b": form_b,
					"cogid": cluster_id,
					"distance_from_identity": distance_from_identity,
					"levenshtein_distance": levenshtein_distance,
					"bigram_distance": bigram_distance,
					"trigram_distance": trigram_distance,
					"combined_distance": combined_distance,
					"same_family": "yes" if family_a == family_b else "no"
				}
				
				distances.append(distances_info)

# Exporting combined borrowings and cognacy validation to TSV
with open("pairwise_distances.tsv", mode="w", encoding="utf8") as file:
	writer = csv.writer(file, delimiter="\t")
	writer.writerow([
		"Doculect A", "Doculect B", "Concept", "Form A", "Form B", "Cogid",
		"Distance from Identity Score", "Levenshtein Distance", "Bigram Distance", "Trigram Distance",
		"Combined Distance", "Same Family?"
	])
	for distance in distances:
		writer.writerow([
			distance["doculect_a"], distance["doculect_b"], distance["concept"],
			distance["form_a"], distance["form_b"], distance["cogid"],
			distance["distance_from_identity"], distance["levenshtein_distance"],
			distance["bigram_distance"], distance["trigram_distance"],
			distance["combined_distance"], distance["same_family"]
		])

# # Calculating distances between doculects
# doculect_distances = defaultdict(list)
#
# for borrowing in borrowings:
# 	source_doculect = borrowing["source_doculect"]
# 	target_doculect = borrowing["target_doculect"]
# 	combined_similarity = borrowing["combined_similarity"]
#
# 	doculect_pair = tuple(sorted([source_doculect, target_doculect]))
# 	doculect_distances[doculect_pair].append(combined_similarity)
#
# average_distances = {
# 	pair: 1 - (sum(distances) / len(distances))
# 	for pair, distances in doculect_distances.items()
# }
#
# # Export to TSV
# with open("doculect_distances.tsv", mode="w", encoding="utf8") as file:
# 	writer = csv.writer(file, delimiter="\t")
# 	writer.writerow(["Doculect A", "Doculect B", "Doculects Distance"])
# 	for (doculect_a, doculect_b), distance in average_distances.items():
# 		writer.writerow([doculect_a, doculect_b, distance])


