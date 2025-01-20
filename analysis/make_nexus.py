"""
Create a nexus file from a Lexibank dataset.
"""
from lingpy import Wordlist, LexStat, Alignments
from lingpy.convert.strings import write_nexus
from lexibank_northperulex import Dataset as NPL

cols = [
	'concept_id', 'concept_name', 'language_id', 'language_name', 'value', 'form', 'segments',
	'glottocode', 'concept_concepticon_id', 'comment', 'language_family', 'language_subgroup'
]

def run(args):
	"""Function runs the creation of a Nexus file."""
	dataset = NPL()
	print(dataset)
	wl = Wordlist.from_cldf(
			str(dataset.cldf_dir.joinpath("cldf-metadata.json").as_posix()),
			columns=cols,
			namespace=(
					("language_id", "doculect"),
					("language_family", "family"),
					("concept_name", "concept"),
					("segments", "tokens"),
					("language_subgroup", "subgroup"),
					("cognacy", "cogid")
			))
	
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
	
	D = {0: [c for c in lex.columns]}  # defines the header
	wlnew = Wordlist(D)
	etd = wlnew.get_etymdict(ref="cogid")
	args.log.info(
		f"Created wordlist with {wlnew.width} languages, {len(etd)} "
		"concepts, and {wlnew.height} cognatesets"
		)
	
	write_nexus(
		wlnew,
		ref="cogid",
		mode="BEAST",
		filename=str(dataset.dir.joinpath('../outputs', 'northperulex.nex'))
		)
	args.log.info("wrote data to file '../outputs/northperulex-beast.nex'")
	wlnew.output(
		"tsv",
		filename=str(dataset.dir.joinpath("../outputs", "northperulex")),
		prettify=False,
		ignore="all")
	args.log.info("wrote wordlist data to file")
