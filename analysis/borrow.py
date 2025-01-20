from lingpy import Wordlist, LexStat, Alignments
from lingpy.compare.strings import ldn_swap, bidist2, tridist2
import csv

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

# Deleting unnecessary tokens
for idx in wl:
	wl[idx, "tokens"] = [x for x in wl[idx, "tokens"] if x != "+"]

# Run AutoCogid
lex = LexStat(wl)
lex.get_scorer(runs=10000)
lex.cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="cogid")

# Align data
alms = Alignments(lex, ref="cogid")
alms.align()
alms.add_entries("morphemes", "tokens", lambda x: "")  # Add aligned morphemes
alms.add_entries("note", "comment", lambda x: x if x else "")  # Add notes

# Borrowing detection with Levenshtein distance and swap check
borrowings = []
for idx in lex:
	source_doculect = lex[idx, 'doculect']
	form = lex[idx, 'form']
	source_family = lex[idx, 'family']
	concept = lex[idx, 'concept']
	cluster_id = lex[idx, 'cogid']
	
	for other_idx in lex:
		if other_idx != idx and lex[other_idx, 'cogid'] == cluster_id:
			target_doculect = lex[other_idx, 'doculect']
			target_family = lex[other_idx, 'family']
			
			if source_doculect != target_doculect:
				borrowed_form = lex[other_idx, 'form']
				source_alignment = alms[idx]
				target_alignment = alms[other_idx]
				
				# Calculate identity score based on alignment
				aligned_columns = 0
				identical_columns = 0
				if source_alignment and target_alignment:
					for seg1, seg2 in zip(source_alignment, target_alignment):
						aligned_columns += 1
						if seg1 == seg2:
							identical_columns += 1
				identity_score = (identical_columns / aligned_columns) if aligned_columns > 0 else 0
				
				# Calculate Levenshtein distance with swap included
				levenshtein_similarity = ldn_swap(form, borrowed_form, normalized=True)
				
				# Calculate Bigram and Trigram Distances
				bigram_distance = bidist2(form, borrowed_form, normalized=True)
				trigram_distance = tridist2(form, borrowed_form, normalized=True)
				
				# Combined Distances
				combined_similarity = (
						0.4 * identity_score +
						0.5 * levenshtein_similarity +
						0.4 * (bigram_distance + trigram_distance)
				) / 4
				
				borrowing_info = {
					"source_doculect": source_doculect,
					"target_doculect": target_doculect,
					"concept": concept,
					"form": form,
					"borrowed_form": borrowed_form,
					"cogid": cluster_id,
					"identity_score": identity_score,
					"levenshtein_similarity": levenshtein_similarity,
                    "bigram_distance": bigram_distance,
                    "trigram_distance": trigram_distance,
					"combined_similarity": combined_similarity,
					"same_family": "yes" if source_family == target_family else "no"
				}
				
				borrowings.append(borrowing_info)
			
# Exporting combined borrowings and cognacy validation to TSV
with open("borrowings.tsv", mode="w", encoding="utf8") as file:
	writer = csv.writer(file, delimiter="\t")
	writer.writerow([
		"Source Doculect", "Target Doculect", "Concept", "Form", "Borrowed Form", "Cogid",
		"Identity Score", "Levenshtein Similarity", "Bigram Distance", "Trigram Distance",
		"Combined Similarity", "Same Family?"
	])
	for borrowing in borrowings:
		writer.writerow([
			borrowing["source_doculect"], borrowing["target_doculect"], borrowing["concept"],
			borrowing["form"], borrowing["borrowed_form"], borrowing["cogid"],
			borrowing["identity_score"], borrowing["levenshtein_similarity"],
			borrowing["bigram_distance"], borrowing["trigram_distance"],
			borrowing["combined_similarity"], borrowing["same_family"]
		])