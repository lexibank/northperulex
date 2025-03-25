from lingpy import Wordlist, LexStat, Alignments
from lingpy.compare.strings import ldn_swap, bidist2, tridist2
import csv
import re
from collections import defaultdict
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

# Align data
alms = Alignments(lex, ref="cogid", transcription="tokens")
alms.align()
alms.add_entries("morphemes","tokens", lambda x: " ".join([y for y in x]), override=True)
alms.add_entries("alignment", "tokens", lambda x: " ".join([y for y in x]), override=True)
alms.add_entries("structure", "tokens",
                 lambda x: tokens2class(x, "cv"))

alms.output("tsv", filename="npl")

# Infer sound correspondances
cop = CoPaR("npl.tsv", transcription="form", ref="cogid")
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

# # Borrowing detection with identity score and distances
# borrowings = []
# for idx in cop_wl:
# 	source_doculect = cop_wl[idx, 'doculect']
# 	form = cop_wl[idx, 'form']
# 	source_family = cop_wl[idx, 'family']
# 	concept = cop_wl[idx, 'concept']
# 	cluster_id = cop_wl[idx, 'cogid']
#
# 	for other_idx in cop_wl:
# 		if other_idx != idx and cop_wl[other_idx, 'cogid'] == cluster_id:
# 			target_doculect = cop_wl[other_idx, 'doculect']
# 			target_family = cop_wl[other_idx, 'family']
#
# 			if source_doculect != target_doculect:
# 				borrowed_form = cop_wl[other_idx, 'form']
# 				source_alignment = alms[idx]
# 				target_alignment = alms[other_idx]
#
# 				# Calculate identity score based on alignment
# 				aligned_columns = 0
# 				identical_columns = 0
# 				if source_alignment and target_alignment:
# 					for seg1, seg2 in zip(source_alignment, target_alignment):
# 						aligned_columns += 1
# 						if seg1 == seg2:
# 							identical_columns += 1
# 				identity_score = (identical_columns / aligned_columns) if aligned_columns > 0 else 0
# 				# Convert identity score into distance
# 				distance_from_identity = 1 - identity_score
#
# 				# Calculate Levenshtein distance with swap included
# 				levenshtein_distance = ldn_swap(form, borrowed_form, normalized=True)
#
# 				# Calculate Bigram and Trigram Distances
# 				bigram_distance = bidist2(form, borrowed_form, normalized=True)
# 				trigram_distance = tridist2(form, borrowed_form, normalized=True)
#
# 				# Combined Distances
# 				combined_distance = (
# 						0.25 * distance_from_identity +
# 						0.25 * levenshtein_distance +
# 						0.25 * bigram_distance +
# 						0.25 * trigram_distance
# 				)
#
# 				borrowing_info = {
# 					"source_doculect": source_doculect,
# 					"target_doculect": target_doculect,
# 					"concept": concept,
# 					"form": form,
# 					"borrowed_form": borrowed_form,
# 					"cogid": cluster_id,
# 					"distance_from_identity": distance_from_identity,
# 					"levenshtein_distance": levenshtein_distance,
# 					"bigram_distance": bigram_distance,
# 					"trigram_distance": trigram_distance,
# 					"combined_distance": combined_distance,
# 					"same_family": "yes" if source_family == target_family else "no"
# 				}
#
# 				borrowings.append(borrowing_info)
#
# # Exporting combined borrowings and cognacy validation to TSV
# with open("borrowings.tsv", mode="w", encoding="utf8") as file:
# 	writer = csv.writer(file, delimiter="\t")
# 	writer.writerow([
# 		"Source Doculect", "Target Doculect", "Concept", "Form", "Borrowed Form", "Cogid",
# 		"Distance from Identity Score", "Levenshtein Distance", "Bigram Distance", "Trigram Distance",
# 		"Combined Distance", "Same Family?"
# 	])
# 	for borrowing in borrowings:
# 		writer.writerow([
# 			borrowing["source_doculect"], borrowing["target_doculect"], borrowing["concept"],
# 			borrowing["form"], borrowing["borrowed_form"], borrowing["cogid"],
# 			borrowing["distance_from_identity"], borrowing["levenshtein_distance"],
# 			borrowing["bigram_distance"], borrowing["trigram_distance"],
# 			borrowing["combined_distance"], borrowing["same_family"]
# 		])
#
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