from lingpy import Alignments
from lingpy.compare.partial import Partial

def run(wordlist):
	D = {0: wordlist.columns}
	for idx in wordlist:
		D[idx] = [wordlist[idx, h] for h in D[0]]
		
	lex = Partial(D, segments='tokens', check=False)
	
	lex = Alignments(lex, ref="cogids")
	lex.align(ref='cogids')
	
	D = {0: wordlist.columns+["alignment"]}
	for idx in lex:
		D[idx] = [lex[idx, h] for h in D[0]]
		
	return lex