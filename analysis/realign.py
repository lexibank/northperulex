"""
This script realigns the wordlist using Lingpy's (List & Forkel 2021)
partial cognate detection and multiple sequence alignment
"""
from lingpy import Alignments
from lingpy.compare.partial import Partial

def run(wordlist):
	data = {0: wordlist.columns}
	for idx in wordlist:
		data[idx] = [wordlist[idx, h] for h in data[0]]
		
	lex = Partial(data, segments='tokens', check=False)
	lex = Alignments(lex, ref='cogids')
	lex.align(ref='cogids')
	
	aligned_data = {0: wordlist.columns + ["alignment"]}
	for idx in lex:
		aligned_data[idx] = [lex[idx, h] for h in aligned_data[0]]
		
	return aligned_data