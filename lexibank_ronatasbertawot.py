import pathlib

import attr
from clldutils.misc import slug
from lingpy import prosodic_string
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language, Lexeme
from pylexibank import FormSpec

from lingpy.sequence.sound_classes import token2class

@attr.s
class CustomLanguage(Language):
    H_orth = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    CV_Segments = attr.ib(default=None)
    ProsodicStructure = attr.ib(default=None)
    FB_Segments = attr.ib(default=None)


def get_clusters(segments):
    out = [segments[0]]
    for i in range(1, len(segments)):
        # can be optimized
        prev, this = token2class(segments[i-1], "cv"), token2class(
                segments[i], "cv")
        if prev == this:
            out[-1] += "."+segments[i]
        else:
            out += [segments[i]]
    return " ".join(out)


def get_front_back_vowels(segments):
    out = []
    for i in range(len(segments)):
# https://en.wikipedia.org/wiki/Automated_Similarity_Judgment_Program#ASJPcode
        asjp_class = token2class(segments[i], "asjp")
        #exchange front vowels with "F" and back ones with "B".
        if asjp_class in "ieE":  # front vowels
            out.append("F")
        elif asjp_class in "uo":  # back vowels
            out.append("B")
        else:
            out.append(segments[i])
    return " ".join(out)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "ronatasbertawot"
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements= [(" ", "")])

    def cmd_makecldf(self, args):

        #add borrowing table
        args.writer.cldf.add_component(
            "BorrowingTable"
            #{"name": "lol", "datatype": "string"},
        )
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = str(i)+"_"+slug(concept["en"])
            concepts[concept["en"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["en"],
                    Concepticon_ID=concept["Concepticon_ID"],
                    Concepticon_Gloss=concept["Concepticon_Gloss"],
                    )
        args.log.info("added concepts")
        #print(concepts)
        # add language
        languages = args.writer.add_languages()
        args.log.info("added languages")

        # read in data
        data = self.raw_dir.read_csv(
            "wot.tsv", delimiter="\t",
        )
        header = data[0]
        cognates = {}
        cogidx = 1
        borrid = 1

        for i in range(1, len(data)):
            cognates = dict(zip(header, data[i]))
            concept = data[i][6]
            eah = ""
            for language in languages:
                cog = cognates.get(language, "").strip()

                if concept not in cognates:
                    cognates[concept] = cogidx
                    cogidx += 1
                cogid = cognates[concept]
                for lex in args.writer.add_forms_from_value(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=cog,
                        Source="wot",
                        Loan=True,
                        Cognacy=cogid
                        ):
                    lex["CV_Segments"] = get_clusters(lex["Segments"])
                    lex["ProsodicStructure"] = prosodic_string(lex["Segments"], _output='cv')
                    lex["FB_Segments"] = get_front_back_vowels(lex["Segments"])
                    if language == "EAH":
                        eah = lex["ID"]

                    if language != "WOT":
                        args.writer.add_cognate(
                                lexeme=lex,
                                Cognateset_ID=cogid,
                                Source="wot"
                                )
                    elif eah:
                        args.writer.objects["BorrowingTable"].append({
                            "ID": f'{borrid}-{lex["Parameter_ID"]}',
                            "Target_Form_ID": eah,
                            "Source_Form_ID": lex["ID"],
                            "Source": lex["Source"]
                            })
                        borrid += 1
