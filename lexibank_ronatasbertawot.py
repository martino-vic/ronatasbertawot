import pathlib

import attr
from clldutils.misc import slug
from lingpy import prosodic_string
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language, Lexeme
from pylexibank import FormSpec
from re import sub

from lingpy.sequence.sound_classes import token2class

@attr.s
class CustomLanguage(Language):
    H_orth = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Orthography = attr.ib(default=None)
    CV_Segments = attr.ib(default=None)
    ProsodicStructure = attr.ib(default=None)
    FB_Segments = attr.ib(default=None)
    FB_Vowel_Harmony = attr.ib(default=None)
    Year = attr.ib(default=None)

# todo: import the next 3 functions from loanpy

def get_clusters(segments):
    """
    Takes a list of phonemes and segments them into consonant and vowel
    clusters, like so: "abcdeaofgh" -> ["a", "bcd", "eao", "fgh"]
    (c) List 2022"""
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
    """
    logic is similar to get_clusters.
    Turns front vowels into "F" and back vowels into "B"
    """
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

def has_harmony(segments):
    """if "F" AND "B" are in segments, the word has NO vowel harmony"""
    return not all(i in get_front_back_vowels(segments) for i in "FB")

def get_orth(orth, language):
    return orth if language == "H" else ""

def get_loan(loan, language):
    return loan == "TRUE" if language == "WOT" else True


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
            idx = str(i)+"_"+slug(concept["H_en"])
            concepts[concept["H_en"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["H_en"],
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
            #print(cognates)
            concept = data[i][7]
            eah = ""
            for language in languages:
                #print(language)
                cog = cognates.get(language, "").strip()
                #print(cog)
                if concept not in cognates:
                    cognates[concept] = cogidx
                    cogidx += 1
                cogid = cognates[concept]
                #print("concept:", concept)
                for lex in args.writer.add_forms_from_value(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=cog,
                        Source="wot",
                        Loan=get_loan(cognates["WOT_loan"], language),
                        Cognacy=cogid,
                        Orthography=get_orth(data[i][0], language),
                        Year=cognates["Year"]
                        ):
                    front_back = get_front_back_vowels(lex["Segments"])
                    lex["CV_Segments"] = get_clusters(lex["Segments"])
                    lex["ProsodicStructure"] = prosodic_string(lex["Segments"], _output='cv')
                    lex["FB_Segments"] = front_back
                    lex["FB_Vowel_Harmony"] = not all(i in front_back for i in "FB")
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
