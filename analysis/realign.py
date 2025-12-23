"""
This script realigns the wordlist using Lingpy's (List & Forkel 2021)
partial cognate detection and multiple sequence alignment, and conducts
the sound correspondence pattern identification with LingRex (List 2018).
"""
import re
from lingpy import Alignments, LexStat, Wordlist
from lingpy.compare.partial import Partial
from lingrex.copar import CoPaR
from lingpy.read.qlc import reduce_alignment
from lingpy.sequence.sound_classes import tokens2class
from lingrex.util import prep_wordlist

def clean_slash(x):
    """
    This function cleans slash annotation from EDICTOR.
    """
    cleaned = []
    for segment in x:
        if "/" in segment:
            after_slash = re.split("/", segment)[1]
            cleaned.append(after_slash)
        else:
            cleaned.append(segment)

    return cleaned


def run(wordlist):
	"""
	This function performs the main pipeline for multiple
	sequence alignment and correspondence pattern analysis.
	"""
	D = {0: wordlist.columns}
	for idx in wordlist:
		D[idx] = [wordlist[idx, h] for h in D[0]]
		
	wl = Wordlist(D)
	wl = prep_wordlist(wl)
	lex = Partial(wl, segments='tokens', check=False)

	alms = Alignments(lex, ref='cogids', transcriptions='tokens')
	alms.align(ref='cogids')
	
	# Perform multiple sequence alignment
	dct = {}
	for idx, msa in alms.msa["cogids"].items():
		msa_reduced = []
		for site in msa["alignment"]:
			reduced = reduce_alignment([site])[0]
			reduced = clean_slash(reduced)
			msa_reduced.append(reduced)
		for i, row in enumerate(msa_reduced):
			dct[msa["ID"][i]] = row

	alms.add_entries("tokens", dct,
					 lambda x: " ".join([y for y in x if y != "-"]),
					 override=True)
	alms.add_entries("alignment", dct,
					 lambda x: " ".join([y for y in x]),
					 override=True)
	alms.add_entries("structure", "tokens",
					 lambda x: tokens2class(x.split(" "), "cv"))
	
	
	# Perform sound correspondence pattern identification
	cop = CoPaR(alms, transcription="form", ref="cogid", min_refs=3)
	cop.get_sites()
	cop.cluster_sites()
	cop.sites_to_pattern()
	cop.add_patterns()
	cop.write_patterns("npl_patterns.tsv")
	
	
	D = {0: wordlist.columns + ["alignment"]}
	for idx in alms:
		D[idx] = [alms[idx, h] for h in D[0]]
		
	return alms