"""
This script filters languages with a total 140 concepts
in common for the purpose of phylogenetic analysis
"""

from lingpy import *
from lingpy.compare.sanity import mutual_coverage_subset

wl = Wordlist("npl.tsv")
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

wl_filtered.output(
    "tsv",
    filename= "npl-filtered"
)