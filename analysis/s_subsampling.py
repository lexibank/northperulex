"""
This script filters languages with at least 130 words
for the purpose of phylogenetic analysis
"""

from lingpy import *
from lingpy.compare.sanity import mutual_coverage_subset
from tabulate import tabulate

wl = Wordlist("npl.tsv")
coverage = wl.coverage()
number_of_languages, pairs = mutual_coverage_subset(wl, 100, concepts='concept')
for number_of_items, languages in pairs:
    print(number_of_items, ','.join(languages))

selected_ls = set().union(*(langs for _, langs in pairs))

selected_ls.discard("Proto-Bora-Muinane")

#print(tabulate([(lang, coverage[lang]) for lang in sorted(selected_ls)],
               #headers=["Doculect", "Words"], tablefmt="pipe"))

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

#print(f"Total rows before: {len(wl)}")
#print(f"Total rows after filtering: {len(wl_filtered)}")