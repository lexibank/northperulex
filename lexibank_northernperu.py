from collections import defaultdict
import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pyedictor import fetch
from lingpy import Wordlist


def unmerge(sequence):
    out = []
    for tok in sequence:
        out += tok.split('.')
    return out


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "northernperu"

    def cmd_download(self, args):
        print("updating ...")
        with open(self.raw_dir.joinpath("raw.tsv"), "w", encoding="utf-8") as f:
            f.write(
                fetch(
                    "northernperu",
                    columns=[
                        "CONCEPT",
                        "DOCULECT",
                        "FORM",
                        "VALUE",
                        "TOKENS",
                        "COGIDS",
                        "ALIGNMENT",
                        "MORPHEMES",
                        "BORROWING",
                        "NOTE"
                    ],
                    base_url="http://lingulist.de/edev"
                )
            )

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.english] = idx

        args.log.info("added concepts")

        # add language
        languages = {}
        sources = defaultdict()
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"]
                    )
            languages[language["ID"]] = language["Name"]
            sources[language["ID"]] = language["Source"]
        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        # ----------
        # This code will be used later on to re-create a single COGID,
        # based on the partial cognacy annoated
        # N = {}
        # for idx, cogids, morphemes in wl.iter_rows("cogids", "morphemes"):
        #     new_cogids = []
        #     if morphemes:
        #         for cogid, morpheme in zip(cogids, morphemes):
        #             if not morpheme.startswith("_"):
        #                 new_cogids += [cogid]
        #     else:
        #         new_cogids = [c for c in cogids if c]

        #     if new_cogids == []:
        #         new_cogids = [c for c in cogids if c]

        #     N[idx] = " ".join([str(x) for x in new_cogids])
        # wl.add_entries("cog", N, lambda x: x, override=True)
        # wl.renumber("cog")  # creates numeric cogid

        # add data
        for (
            idx,
            concept,
            language,
            form
            # value,
            # tokens,
            # cogid,
            # cogids,
            # alignment,
            # morphemes,
            # borrowing,
            # note
        ) in pb(
            wl.iter_rows(
                "concept",
                "doculect",
                "form"
                # "value",
                # "tokens",
                # "cogid",
                # "cogids",
                # "alignment",
                # "morphemes",
                # "borrowing",
                # "note"
            ),
            desc="cldfify"
        ):
            if morphemes == []:
                morphemes = ["?"]
            if language not in languages:
                errors.add(("language", language))
            elif concept not in concepts:
                errors.add(("concept", concept))
            else:
                # lexeme = args.writer.add_form_with_segments(
                args.writer.add_forms_from_value(
                    Parameter_ID=concepts[concept],
                    Language_ID=language,
                    Form=form.strip(),
                    Value=form.strip(),  # value.strip() or 
                    # Cognacy=cogid,
                    # Partial_Cognacy=" ".join([str(x) for x in cogids]),
                    # Alignment=" ".join(alignment),
                    # Morphemes=" ".join(morphemes),
                    # Comment=note,
                    # Borrowing=borrowing,
                    Source=sources[language]
                )

                # args.writer.add_cognate(
                #     lexeme=lexeme,
                #     Cognateset_ID=cogid,
                #     Alignment=alignment,
                #     Alignment_Method="false",
                #     Alignment_Source="expert"
                #     )
