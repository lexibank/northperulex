from lingpy import *
from lingrex.util import add_structure
from lingrex.copar import CoPaR

alms = Alignments("npl_filtered.tsv", ref="cogids", transcription="form")
alms.align()
add_structure(alms, model="cv")
alms.output('tsv', filename="npl-aligned", ignore="all", prettify=False)

cop = CoPaR("npl-aligned.tsv", min_refs=5, ref='cogids', transcription="form")
cop.get_sites()
cop.cluster_sites()
cop.add_patterns()
cop.write_patterns("npl-patterns")