"""
This scripts filters languages with at least 95 words
for the purpose of phylogenetic analysis
"""

from lingpy import *
from tabulate import tabulate

wl = Wordlist("npl.tsv")
coverage = wl.coverage()

selected_ls = {lang for lang, count in coverage.items() if count >= 95
               and lang != "Proto-Bora-Muinane"}

print(tabulate([(lang, coverage[lang]) for lang in sorted(selected_ls)],
               headers=["Doculect", "Words"], tablefmt="pipe"))

D = {0: [c for c in wl.columns]}
for idx in wl:
    if (
        wl[idx, "doculect"] in selected_ls
    ):
        D[idx] = [wl[idx, c] for c in D[0]]
        
wl_filtered = Wordlist(D)

wl_filtered.output(
    "tsv",
    filename= "npl_filtered"
)

print(f"Total rows before: {len(wl)}")
print(f"Total rows after filtering: {len(wl_filtered)}")