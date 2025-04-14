from lingpy import LexStat, Alignments
from lingpy.compare.partial import Partial
from lingpy.sequence.sound_classes import tokens2class


def run(wl):
    # Deleting unnecessary tokens with clean_slash
    for idx in wl:
        wl[idx, "tokens"] = [x.split("/")[1] if "/" in x else x for x in wl[idx, "tokens"]]

    # Run AutoCogid
    lex = LexStat(wl)
    lex.get_scorer(runs=10000)
    lex.cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="cogid")

    # Get morpheme segmentation
    parcog = Partial(lex, segments='tokens')
    parcog.partial_cluster(threshold=0.55, method="lexstat", ref="cogids")

    # Align data
    alms = Alignments(parcog, ref="cogids", transcription="tokens")
    alms.align(ref="cogids")
    alms.add_entries("morphemes", "tokens", lambda x: " ".join(list(x)), override=True)
    alms.add_entries("alignment", "tokens", lambda x: " ".join(list(x)), override=True)
    alms.add_entries("structure", "tokens", lambda x: tokens2class(x, "cv"))

    return alms
